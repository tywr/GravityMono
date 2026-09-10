"""Generate font."""

import os
import importlib
import inspect
import math
import pkgutil

import pathops
from fontTools.fontBuilder import FontBuilder
from fontTools.misc.timeTools import timestampNow
from fontTools.pens.t2CharStringPen import T2CharStringPen
from ttfautohint import ttfautohint

from fontTools.ttLib.tables.otTables import (
    AlternateSubst,
    GSUB,
    ChainContextSubst,
    Coverage,
    DefaultLangSys,
    Feature,
    FeatureList,
    FeatureRecord,
    Ligature,
    LigatureSubst,
    Lookup,
    LookupList,
    Script,
    ScriptList,
    ScriptRecord,
    SingleSubst,
    SubstLookupRecord,
)
from fontTools.ttLib import newTable

from config import FontConfig as fc
from config import DrawConfig
from glyphs import Glyph, LigatureGlyph, ContextualLigatureGlyph

import glyphs


def discover_glyphs():
    """Recursively import all modules under glyphs/ and return Glyph subclasses.

    Walks subpackages to arbitrary depth. Import errors propagate so a
    broken module aborts discovery rather than being silently skipped.
    """

    def walk(pkg):
        for info in pkgutil.iter_modules(pkg.__path__, pkg.__name__ + "."):
            module = importlib.import_module(info.name)
            if info.ispkg:
                walk(module)

    walk(glyphs)

    def all_subclasses(cls):
        result = []
        for sub in cls.__subclasses__():
            if not inspect.isabstract(sub):
                result.append(sub)
            result.extend(all_subclasses(sub))
        return result

    return [cls() for cls in all_subclasses(Glyph)]


def draw_notdef(pen):
    pen.moveTo((50, 0))
    pen.lineTo((50, 700))
    pen.lineTo((450, 700))
    pen.lineTo((450, 0))
    pen.closePath()


def simplify_glyph(glyph, **kwargs):
    """Draw a glyph through pathops and return the simplified pathops.Path."""
    path = pathops.Path()
    glyph.draw(pathops.PathPen(path), **kwargs)
    return pathops.simplify(path, clockwise=False, keep_starting_points=True)


def record_glyph(glyph, **kwargs):
    path = simplify_glyph(glyph, **kwargs)
    pen = T2CharStringPen(fc.window_width, None)
    path.draw(pen)
    return pen.getCharString()


def skew_path(path, angle_deg):
    """Apply an italic skew (horizontal shear) to a pathops.Path."""
    skew = math.tan(math.radians(angle_deg))
    skewed = pathops.Path()
    pen = pathops.PathPen(skewed)
    for verb, points in path:
        transformed = tuple((x + y * skew, y) for x, y in points)
        if verb == pathops.PathVerb.MOVE:
            pen.moveTo(*transformed)
        elif verb == pathops.PathVerb.LINE:
            pen.lineTo(*transformed)
        elif verb == pathops.PathVerb.CUBIC:
            pen.curveTo(*transformed)
        elif verb == pathops.PathVerb.CLOSE:
            pen.closePath()
    return skewed


def select_style_glyphs(all_glyphs, italic):
    """Select one default and the applicable alternates for each style."""
    defaults = {}
    by_unicode = {}
    for glyph in all_glyphs:
        if glyph.unicode:
            by_unicode.setdefault(int(glyph.unicode, 16), []).append(glyph)

    for code, glyphs_for_code in by_unicode.items():
        candidates = [
            glyph
            for glyph in glyphs_for_code
            if not glyph.font_feature
            and not glyph.italic_only
            and (glyph.default_italic if italic else not glyph.default_italic)
        ]
        if not candidates and italic:
            candidates = [
                glyph
                for glyph in glyphs_for_code
                if not glyph.font_feature
                and not glyph.default_italic
                and not glyph.italic_only
            ]
        if not candidates:
            raise ValueError(
                f"Expected one {'italic' if italic else 'regular'} default "
                f"for U+{code:04X}, found none"
            )
        defaults[code] = candidates[-1]

    active = list(defaults.values())
    for glyph in all_glyphs:
        if not glyph.unicode:
            active.append(glyph)
        elif glyph.font_feature:
            code = int(glyph.unicode, 16)
            has_italic_default = defaults[code].default_italic
            if italic:
                if glyph.italic_only or not has_italic_default:
                    active.append(glyph)
            elif not glyph.italic_only:
                active.append(glyph)

    return active, {glyph.name for glyph in defaults.values()}


def _coverage(glyphs):
    """Build a Coverage table from a glyph name or list of glyph names."""
    cov = Coverage()
    cov.glyphs = list(glyphs) if isinstance(glyphs, (list, tuple)) else [glyphs]
    return cov


def _chain_subtable(input_seq, backtrack, lookahead, subst_records):
    """Build a format-3 ChainContextSubst subtable.

    Each element of `input_seq`, `backtrack`, `lookahead` is either a glyph
    name (one-glyph coverage) or a list of glyph names (any-of coverage).
    Backtrack is stored in reverse sequence order per the OpenType spec
    (closest-to-input first).
    """
    st = ChainContextSubst()
    st.Format = 3
    st.BacktrackGlyphCount = len(backtrack)
    st.BacktrackCoverage = [_coverage(g) for g in reversed(backtrack)]
    st.InputGlyphCount = len(input_seq)
    st.InputCoverage = [_coverage(g) for g in input_seq]
    st.LookAheadGlyphCount = len(lookahead)
    st.LookAheadCoverage = [_coverage(g) for g in lookahead]
    st.SubstCount = len(subst_records)
    st.SubstLookupRecord = subst_records
    return st


def build_gsub(glyph_names, ligature_glyphs, alternate_glyphs, cmap):
    """Build a GSUB table with ligature and alternate substitutions."""
    gsub_table = newTable("GSUB")
    gsub = GSUB()
    gsub.Version = 0x00010000
    gsub_table.table = gsub

    lookups = []
    feature_records = []

    def add_feature(tag, lookup_indices):
        for record in feature_records:
            if record.FeatureTag == tag:
                record.Feature.LookupListIndex.extend(lookup_indices)
                record.Feature.LookupCount = len(record.Feature.LookupListIndex)
                return

        feature = Feature()
        feature.FeatureParams = None
        feature.LookupListIndex = list(lookup_indices)
        feature.LookupCount = len(lookup_indices)

        record = FeatureRecord()
        record.FeatureTag = tag
        record.Feature = feature
        feature_records.append(record)

    def ligature_feature_tags(glyph):
        tags = glyph.feature_tags
        if isinstance(tags, str):
            tags = (tags,)
        tags = tuple(dict.fromkeys(tags))
        if not tags:
            raise ValueError(f"Ligature {glyph.name!r} must have a feature tag")
        for tag in tags:
            if not isinstance(tag, str) or len(tag) != 4:
                raise ValueError(
                    f"Invalid OpenType feature tag {tag!r} on {glyph.name!r}"
                )
        return tags

    # Reverse cmap: unicode int -> base glyph name
    base_by_unicode = {unicode_val: name for unicode_val, name in cmap.items()}

    # Build alternate substitution lookups grouped by feature tag
    feature_lookups = {}
    for g in alternate_glyphs:
        if g.name not in glyph_names or not g.unicode:
            continue
        base_name = base_by_unicode.get(int(g.unicode, 16))
        if not base_name:
            continue
        for tag, alternate_index in g.font_feature.items():
            alternatives = feature_lookups.setdefault(tag, {}).setdefault(
                base_name, {}
            )
            if alternate_index in alternatives:
                raise ValueError(
                    f"Duplicate alternate index {alternate_index} for "
                    f"{base_name!r} in feature {tag!r}"
                )
            alternatives[alternate_index] = g.name

    for tag in sorted(feature_lookups):
        indexed_alternatives = feature_lookups[tag]
        if all(
            set(alternatives) == {1}
            for alternatives in indexed_alternatives.values()
        ):
            subst = SingleSubst()
            subst.mapping = {
                base_name: alternatives[1]
                for base_name, alternatives in indexed_alternatives.items()
            }
            lookup_type = 1
        else:
            subst = AlternateSubst()
            lookup_type = 3
            subst.alternates = {}
            for base_name, alternatives in indexed_alternatives.items():
                expected = set(range(1, max(alternatives) + 1))
                if set(alternatives) != expected:
                    raise ValueError(
                        f"Alternate indices for {base_name!r} in feature {tag!r} "
                        f"must be consecutive from 1"
                    )
                subst.alternates[base_name] = [
                    alternatives[index] for index in sorted(alternatives)
                ]

        lookup = Lookup()
        lookup.LookupType = lookup_type
        lookup.LookupFlag = 0
        lookup.SubTableCount = 1
        lookup.SubTable = [subst]

        lookup_idx = len(lookups)
        lookups.append(lookup)
        add_feature(tag, [lookup_idx])

    # Split ligatures: regular (unconditional) vs contextual (neighbor-gated)
    regular_ligs = [
        g
        for g in ligature_glyphs
        if not isinstance(g, ContextualLigatureGlyph) and g.name in glyph_names
    ]
    contextual_ligs = [
        g
        for g in ligature_glyphs
        if isinstance(g, ContextualLigatureGlyph) and g.name in glyph_names
    ]

    # Build regular ligature lookups, grouped by their OpenType feature.
    regular_ligs_by_feature = {}
    for g in regular_ligs:
        for tag in ligature_feature_tags(g):
            regular_ligs_by_feature.setdefault(tag, []).append(g)

    for tag in sorted(regular_ligs_by_feature):
        lig_by_first = {}
        for g in regular_ligs_by_feature[tag]:
            first = g.components[0]
            rest = g.components[1:]
            lig = Ligature()
            lig.LigGlyph = g.name
            lig.Component = rest
            lig.CompCount = len(g.components)
            lig_by_first.setdefault(first, []).append(lig)

        subst = LigatureSubst()
        subst.ligatures = lig_by_first

        lookup = Lookup()
        lookup.LookupType = 4  # Ligature substitution
        lookup.LookupFlag = 0
        lookup.SubTableCount = 1
        lookup.SubTable = [subst]

        lookup_idx = len(lookups)
        lookups.append(lookup)
        add_feature(tag, [lookup_idx])

    # Build contextual ligature lookups (`calt`).
    # For each contextual ligature, emit a nested LookupType 4 that does the
    # actual substitution, plus a LookupType 6 chain-context wrapper with
    # ignore-subtables that suppress the match when a forbidden neighbor
    # appears before or after the input sequence. Longer ligatures are
    # referenced first so the shaper tries them before shorter ones.
    contextual_ligs.sort(key=lambda g: -len(g.components))
    contextual_lookup_indices = {}
    for g in contextual_ligs:
        lig = Ligature()
        lig.LigGlyph = g.name
        lig.Component = g.components[1:]
        lig.CompCount = len(g.components)

        nested_subst = LigatureSubst()
        nested_subst.ligatures = {g.components[0]: [lig]}

        nested_lookup = Lookup()
        nested_lookup.LookupType = 4
        nested_lookup.LookupFlag = 0
        nested_lookup.SubTableCount = 1
        nested_lookup.SubTable = [nested_subst]
        nested_idx = len(lookups)
        lookups.append(nested_lookup)

        chain_lookup = Lookup()
        chain_lookup.LookupType = 6
        chain_lookup.LookupFlag = 0
        subtables = []
        if g.forbidden_neighbors:
            subtables.append(
                _chain_subtable(
                    input_seq=g.components,
                    backtrack=[],
                    lookahead=[g.forbidden_neighbors],
                    subst_records=[],
                )
            )
            subtables.append(
                _chain_subtable(
                    input_seq=g.components,
                    backtrack=[g.forbidden_neighbors],
                    lookahead=[],
                    subst_records=[],
                )
            )
        rec = SubstLookupRecord()
        rec.SequenceIndex = 0
        rec.LookupListIndex = nested_idx
        subtables.append(
            _chain_subtable(
                input_seq=g.components,
                backtrack=[],
                lookahead=[],
                subst_records=[rec],
            )
        )
        chain_lookup.SubTable = subtables
        chain_lookup.SubTableCount = len(subtables)

        lookup_index = len(lookups)
        lookups.append(chain_lookup)
        for tag in ligature_feature_tags(g):
            contextual_lookup_indices.setdefault(tag, []).append(lookup_index)

    for tag, lookup_indices in sorted(contextual_lookup_indices.items()):
        add_feature(tag, lookup_indices)

    gsub.LookupList = LookupList()
    gsub.LookupList.LookupCount = len(lookups)
    gsub.LookupList.Lookup = lookups

    gsub.FeatureList = FeatureList()
    gsub.FeatureList.FeatureCount = len(feature_records)
    gsub.FeatureList.FeatureRecord = feature_records

    # Script: DFLT with default lang sys referencing all features
    lang_sys = DefaultLangSys()
    lang_sys.ReqFeatureIndex = 0xFFFF
    lang_sys.FeatureIndex = list(range(len(feature_records)))
    lang_sys.FeatureCount = len(feature_records)

    script = Script()
    script.DefaultLangSys = lang_sys
    script.LangSysRecord = []
    script.LangSysCount = 0

    script_record = ScriptRecord()
    script_record.ScriptTag = "DFLT"
    script_record.Script = script

    gsub.ScriptList = ScriptList()
    gsub.ScriptList.ScriptCount = 1
    gsub.ScriptList.ScriptRecord = [script_record]

    return gsub_table


WEIGHT_NAMES = {
    100: "Thin",
    200: "ExtraLight",
    300: "Light",
    400: "Regular",
    500: "Medium",
    600: "SemiBold",
    700: "Bold",
}


def _style_metadata(weight, italic):
    """Compute style name, PS name, name table entries, and OS/2 flags for a weight/italic combination."""
    if weight not in WEIGHT_NAMES:
        raise ValueError(
            f"Unsupported weight {weight}; must be one of {sorted(WEIGHT_NAMES)}"
        )

    weight_name = WEIGHT_NAMES[weight]
    if weight == 400:
        style_name = "Italic" if italic else "Regular"
    elif weight == 700:
        style_name = "Bold Italic" if italic else "Bold"
    else:
        style_name = f"{weight_name} Italic" if italic else weight_name

    ps_style_name = style_name.replace(" ", "")
    ps_name = f"{fc.family_name}-{ps_style_name}"
    full_name = f"{fc.family_name} {style_name}"

    # RIBBI = Regular/Bold/Italic/BoldItalic — macOS style-links these under one family.
    # Non-RIBBI weights get their own family name plus typographic family/subfamily
    # (name IDs 16/17) so modern apps can still group them.
    is_ribbi = weight in (400, 700)
    if is_ribbi:
        name_table = {
            "familyName": fc.family_name,
            "styleName": style_name,
            "uniqueFontIdentifier": ps_name,
            "fullName": full_name,
            "version": "Version 1.000",
            "psName": ps_name,
        }
    else:
        legacy_family = f"{fc.family_name} {weight_name}"
        legacy_sub = "Italic" if italic else "Regular"
        name_table = {
            "familyName": legacy_family,
            "styleName": legacy_sub,
            "uniqueFontIdentifier": ps_name,
            "fullName": full_name,
            "version": "Version 1.000",
            "psName": ps_name,
            "typographicFamily": fc.family_name,
            "typographicSubfamily": style_name,
        }

    fs_selection = 0x0000
    mac_style = 0x0000
    if weight == 700:
        fs_selection |= 0x0020  # BOLD
        mac_style |= 0x0001
    if italic:
        fs_selection |= 0x0001  # ITALIC
        mac_style |= 0x0002
    if fs_selection == 0:
        fs_selection |= 0x0040  # REGULAR

    return style_name, ps_style_name, name_table, fs_selection, mac_style


def write_web_fonts(src_path, woff=True, woff2=True, out_root="fonts"):
    """Generate WOFF/WOFF2 web fonts from an already-built TTF/OTF file.

    WOFF and WOFF2 are just compressed wrappers around the same sfnt data,
    so we reload the saved font and re-save it with the matching flavor into
    `{out_root}/woff/` and `{out_root}/woff2/`.
    """
    from fontTools.ttLib import TTFont

    base = os.path.splitext(os.path.basename(src_path))[0]
    for flavor, enabled in (("woff", woff), ("woff2", woff2)):
        if not enabled:
            continue
        out_dir = f"{out_root}/{flavor}"
        os.makedirs(out_dir, exist_ok=True)
        out_path = f"{out_dir}/{base}.{flavor}"
        font = TTFont(src_path)
        font.flavor = flavor
        font.save(out_path)
        font.close()
        print(f"Font saved to {out_path}")


def build_font(
    output_path=None,
    weight=400,
    italic=False,
    otf=True,
    ttf=True,
    woff=False,
    woff2=False,
    out_root="fonts",
):
    style_name, ps_style_name, name_table, fs_selection, mac_style = _style_metadata(
        weight, italic
    )

    if output_path is None:
        if otf:
            os.makedirs(f"{out_root}/otf/", exist_ok=True)
        if ttf:
            os.makedirs(f"{out_root}/ttf/", exist_ok=True)
        fname = fc.family_name.replace(" ", "")
        output_path = f"{out_root}/otf/{fname}-{ps_style_name}.otf"

    if weight != 400:
        dc = DrawConfig.weight(w=weight)
    elif italic:
        dc = DrawConfig.for_italic()
    else:
        dc = DrawConfig()
    dc.italic = italic

    all_glyphs = discover_glyphs()

    active_glyphs, promoted = select_style_glyphs(all_glyphs, italic)

    cmap = {0x20: "space"}
    ligature_glyphs = []
    alternate_glyphs = []
    for g in active_glyphs:
        if g.font_feature and g.name not in promoted:
            alternate_glyphs.append(g)
        elif g.unicode:
            cmap[int(g.unicode, 16)] = g.name
        if isinstance(g, LigatureGlyph):
            ligature_glyphs.append(g)

    if otf:
        _build_otf(
            output_path,
            weight,
            italic,
            active_glyphs,
            cmap,
            dc,
            ligature_glyphs,
            alternate_glyphs,
            style_name,
            ps_style_name,
            name_table,
            fs_selection,
            mac_style,
        )

    ttf_path = output_path.replace(".otf", ".ttf").replace("/otf", "/ttf")
    if ttf:
        build_ttf(
            ttf_path,
            weight,
            italic,
            active_glyphs,
            cmap,
            dc,
            ligature_glyphs,
            alternate_glyphs,
        )

    if woff or woff2:
        # Prefer the (autohinted) TTF as the web-font source, else the OTF.
        web_src = ttf_path if ttf else output_path if otf else None
        if web_src:
            write_web_fonts(web_src, woff=woff, woff2=woff2, out_root=out_root)


def _build_otf(
    output_path,
    weight,
    italic,
    active_glyphs,
    cmap,
    dc,
    ligature_glyphs,
    alternate_glyphs,
    style_name,
    ps_style_name,
    name_table,
    fs_selection,
    mac_style,
):
    # Build charstrings
    notdef_pen = T2CharStringPen(fc.window_width, None)
    draw_notdef(notdef_pen)

    space_pen = T2CharStringPen(fc.window_width, None)

    charstrings = {
        ".notdef": notdef_pen.getCharString(),
        "space": space_pen.getCharString(),
    }
    for g in active_glyphs:
        path = simplify_glyph(g, dc=dc)
        if italic:
            path = skew_path(path, fc.italic_angle)
        pen = T2CharStringPen(fc.window_width, None)
        path.draw(pen)
        charstrings[g.name] = pen.getCharString()

    glyph_names = list(charstrings.keys())

    fb = FontBuilder(fc.units_per_em, isTTF=False)
    fb.setupGlyphOrder(glyph_names)
    fb.setupCharacterMap(cmap)
    # Alignment zones for CFF hinting
    # BlueValues: pairs of [flat_edge, overshoot_edge] for zones at or above baseline
    # OtherBlues: pairs for zones below baseline (descender)
    ov = dc.v_overshoot
    blue_values = [
        -ov,
        0,  # baseline (overshoot below)
        fc.x_height,
        fc.x_height + ov,  # x-height
        fc.cap,
        fc.cap + ov,  # cap height
        fc.ascent,
        fc.ascent + ov,  # ascender
    ]
    other_blues = [
        fc.descent - ov,
        fc.descent,  # descender
    ]

    fb.setupCFF(
        psName=f"{fc.family_name}-{ps_style_name}",
        fontInfo={"FullName": f"{fc.family_name} {style_name}"},
        charStringsDict=charstrings,
        privateDict={
            "BlueValues": blue_values,
            "OtherBlues": other_blues,
            "BlueShift": 7,
            "BlueFuzz": 1,
        },
    )
    # Ligature glyphs get wider advance width based on number_characters
    glyph_by_name = {g.name: g for g in active_glyphs}
    metrics = {}
    for name in glyph_names:
        g = glyph_by_name.get(name)
        n = g.number_characters if g else 1
        metrics[name] = (fc.window_width * n, 0)
    fb.setupHorizontalMetrics(metrics)
    fb.setupHorizontalHeader(ascent=fc.window_ascent, descent=-abs(fc.window_descent))
    fb.setupNameTable(name_table)

    fb.setupOS2(
        sTypoAscender=fc.ascent,
        sTypoDescender=fc.descent,
        sTypoLineGap=50,
        usWinAscent=fc.window_ascent,
        usWinDescent=abs(fc.window_descent),
        sxHeight=fc.x_height,
        sCapHeight=fc.cap,
        fsType=0,
        fsSelection=fs_selection,
        usWeightClass=weight,
    )
    ital_angle = -fc.italic_angle if italic else 0
    fb.setupPost(isFixedPitch=1, italicAngle=ital_angle)
    timestamp = timestampNow()
    fb.setupHead(
        unitsPerEm=fc.units_per_em,
        macStyle=mac_style,
        created=timestamp,
        modified=timestamp,
    )

    # GSUB table for ligatures and alternates
    if ligature_glyphs or alternate_glyphs:
        fb.font["GSUB"] = build_gsub(
            glyph_names, ligature_glyphs, alternate_glyphs, cmap
        )

    # Dummy DSIG so macOS validators don't complain
    dsig = newTable("DSIG")
    dsig.ulVersion = 1
    dsig.usFlag = 0
    dsig.usNumSigs = 0
    dsig.signatureRecords = []
    fb.font["DSIG"] = dsig

    fb.font.save(output_path)
    print(f"Font saved to {output_path}")


def build_ttf(
    output_path, weight, italic, all_glyphs, cmap, dc, ligature_glyphs, alternate_glyphs
):
    """Build a TTF font with quadratic outlines from scratch."""
    from fontTools.pens.cu2quPen import Cu2QuPen
    from fontTools.pens.ttGlyphPen import TTGlyphPen

    _, _, name_table, fs_selection, mac_style = _style_metadata(weight, italic)

    def record_ttf_glyph(glyph):
        path = simplify_glyph(glyph, dc=dc)
        if italic:
            path = skew_path(path, fc.italic_angle)
        ttf_pen = TTGlyphPen(None)
        cu2qu_pen = Cu2QuPen(ttf_pen, max_err=1.0, reverse_direction=True)
        path.draw(cu2qu_pen)
        return ttf_pen.glyph()

    # .notdef
    notdef_pen = TTGlyphPen(None)
    draw_notdef(notdef_pen)

    # space (empty)
    space_pen = TTGlyphPen(None)
    space_pen.glyph()  # finalize empty glyph

    glyph_table = {".notdef": notdef_pen.glyph(), "space": TTGlyphPen(None).glyph()}
    for g in all_glyphs:
        glyph_table[g.name] = record_ttf_glyph(g)

    glyph_names = list(glyph_table.keys())

    fb = FontBuilder(fc.units_per_em, isTTF=True)
    fb.setupGlyphOrder(glyph_names)
    fb.setupCharacterMap(cmap)
    fb.setupGlyf(glyph_table)
    # LSB must match glyf xMin for correct TTF rendering
    glyph_by_name = {g.name: g for g in all_glyphs}
    metrics = {}
    for name in glyph_names:
        ttf_g = glyph_table[name]
        lsb = ttf_g.xMin if hasattr(ttf_g, "xMin") and ttf_g.numberOfContours > 0 else 0
        src_g = glyph_by_name.get(name)
        n = src_g.number_characters if src_g else 1
        metrics[name] = (fc.window_width * n, lsb)
    fb.setupHorizontalMetrics(metrics)
    fb.setupHorizontalHeader(ascent=fc.window_ascent, descent=-abs(fc.window_descent))
    fb.setupNameTable(name_table)

    fb.setupOS2(
        sTypoAscender=fc.ascent,
        sTypoDescender=fc.descent,
        sTypoLineGap=50,
        usWinAscent=fc.window_ascent,
        usWinDescent=abs(fc.window_descent),
        sxHeight=fc.x_height,
        sCapHeight=fc.cap,
        fsType=0,
        fsSelection=fs_selection,
        usWeightClass=weight,
    )
    ital_angle = -fc.italic_angle if italic else 0
    fb.setupPost(isFixedPitch=1, italicAngle=ital_angle)
    timestamp = timestampNow()
    fb.setupHead(
        unitsPerEm=fc.units_per_em,
        macStyle=mac_style,
        created=timestamp,
        modified=timestamp,
    )

    # GSUB table for ligatures and alternates
    if ligature_glyphs or alternate_glyphs:
        fb.font["GSUB"] = build_gsub(
            glyph_names, ligature_glyphs, alternate_glyphs, cmap
        )

    dsig = newTable("DSIG")
    dsig.ulVersion = 1
    dsig.usFlag = 0
    dsig.usNumSigs = 0
    dsig.signatureRecords = []
    fb.font["DSIG"] = dsig

    fb.font.save(output_path)
    ttfautohint(in_file=output_path, out_file=output_path)
    print(f"Font saved to {output_path}")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Generate Nordwand Mono font files")
    fmt = parser.add_mutually_exclusive_group()
    fmt.add_argument("--ttf", action="store_true", help="Generate only TTF files")
    fmt.add_argument("--otf", action="store_true", help="Generate only OTF files")
    parser.add_argument(
        "--web-font",
        action="store_true",
        help="Also generate WOFF and WOFF2 files",
    )
    parser.add_argument(
        "--config",
        metavar="FILE.yml",
        help="YAML file whose values overwrite the default FontConfig values",
    )
    args = parser.parse_args()

    out_root = "fonts"
    if args.config:
        from config import load_config

        applied = load_config(args.config)
        print(f"Loaded config overrides from {args.config}: {applied}")
        # Custom builds are written under ./custom-fonts/{font_name} so they
        # don't clobber the default fonts/ output.
        font_name = fc.family_name.replace(" ", "")
        out_root = f"custom-fonts/{font_name}"
        print(f"Writing custom fonts to ./{out_root}/")

    build_otf = not args.ttf
    build_ttf_flag = not args.otf

    for w in [100, 200, 300, 400, 500, 600, 700]:
        build_font(
            weight=w,
            otf=build_otf,
            ttf=build_ttf_flag,
            woff=args.web_font,
            woff2=args.web_font,
            out_root=out_root,
        )
        build_font(
            weight=w,
            italic=True,
            otf=build_otf,
            ttf=build_ttf_flag,
            woff=args.web_font,
            woff2=args.web_font,
            out_root=out_root,
        )
