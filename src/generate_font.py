"""Generate font."""

import importlib
import pkgutil

import pathops
from fontTools.fontBuilder import FontBuilder
from fontTools.pens.t2CharStringPen import T2CharStringPen

from config import FontConfig as fc
from glyph import Glyph

import glyphs.letters

STROKE = 70


def discover_glyphs():
    """Recursively import all modules under glyphs/ and return Glyph subclasses."""
    def on_error(name):
        raise ImportError(f"Failed to import {name}")

    for pkg in [glyphs.letters]:
        for importer, modname, ispkg in pkgutil.walk_packages(
            pkg.__path__, pkg.__name__ + ".", onerror=on_error
        ):
            importlib.import_module(modname)
    return [cls() for cls in Glyph.__subclasses__()]


def draw_notdef(pen):
    pen.moveTo((50, 0))
    pen.lineTo((50, 700))
    pen.lineTo((450, 700))
    pen.lineTo((450, 0))
    pen.closePath()


def record_glyph(glyph, **kwargs):
    path = pathops.Path()
    pen = pathops.PathPen(path)
    glyph.draw(pathops.PathPen(path), **kwargs)
    path = pathops.simplify(path, clockwise=False, keep_starting_points=True)

    pen = T2CharStringPen(fc.width, None)
    path.draw(pen)
    return pen.getCharString()


def build_font(output_path=f"{fc.family_name}.otf"):
    all_glyphs = discover_glyphs()

    cmap = {0x20: "space"}
    for g in all_glyphs:
        cmap[int(g.unicode, 16)] = g.name

    # Build charstrings
    notdef_pen = T2CharStringPen(fc.width, None)
    draw_notdef(notdef_pen)

    space_pen = T2CharStringPen(fc.width, None)

    charstrings = {
        ".notdef": notdef_pen.getCharString(),
        "space": space_pen.getCharString(),
    }
    for g in all_glyphs:
        charstrings[g.name] = record_glyph(g, stroke=STROKE)

    glyph_names = list(charstrings.keys())

    fb = FontBuilder(fc.units_per_em, isTTF=False)
    fb.setupGlyphOrder(glyph_names)
    fb.setupCharacterMap(cmap)
    fb.setupCFF(
        psName=f"{fc.family_name}-Regular",
        fontInfo={"FullName": f"{fc.family_name} Regular"},
        charStringsDict=charstrings,
        privateDict={},
    )
    fb.setupHorizontalMetrics({name: (fc.width, 0) for name in glyph_names})
    fb.setupHorizontalHeader(ascent=fc.window_ascent, descent=-abs(fc.window_descent))
    fb.setupNameTable(
        {
            "familyName": fc.family_name,
            "styleName": "Regular",
            "uniqueFontIdentifier": f"{fc.family_name}-Regular",
            "fullName": f"{fc.family_name} Regular",
            "version": "Version 1.000",
            "psName": f"{fc.family_name}-Regular",
        }
    )
    fb.setupOS2(
        sTypoAscender=fc.ascent,
        sTypoDescender=fc.descent,
        sTypoLineGap=50,
        usWinAscent=fc.window_ascent,
        usWinDescent=abs(fc.window_descent),
        sxHeight=fc.x_height,
        sCapHeight=fc.cap,
        fsType=0,
    )
    fb.setupPost(isFixedPitch=1)
    fb.setupHead(unitsPerEm=fc.units_per_em)

    # Dummy DSIG so macOS validators don't complain
    from fontTools.ttLib import newTable

    dsig = newTable("DSIG")
    dsig.ulVersion = 1
    dsig.usFlag = 0
    dsig.usNumSigs = 0
    dsig.signatureRecords = []
    fb.font["DSIG"] = dsig

    fb.font.save(output_path)
    print(f"Font saved to {output_path}")


if __name__ == "__main__":
    build_font()
