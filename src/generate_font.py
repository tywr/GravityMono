"""Generate OrbitonMono OTF font with CFF outlines."""

from fontTools.fontBuilder import FontBuilder
from fontTools.pens.t2CharStringPen import T2CharStringPen

from config import FontConfig as fc
from glyphs.letters.a import draw_a
from glyphs.letters.o import draw_o
from glyphs.letters.b import draw_b
from glyphs.letters.c import draw_c
from glyphs.letters.d import draw_d
from glyphs.letters.e import draw_e
from glyphs.letters.f import draw_f

STROKE = 60


def draw_notdef(pen):
    pen.moveTo((50, 0))
    pen.lineTo((50, 700))
    pen.lineTo((450, 700))
    pen.lineTo((450, 0))
    pen.closePath()


def record_glyph(draw_fn):
    pen = T2CharStringPen(fc.width, None)
    draw_fn(pen, stroke=STROKE)
    return pen.getCharString()


def build_font(output_path="OrbitonMono.otf"):
    cmap = {
        0x20: "space",
        0x61: "a",
        0x62: "b",
        0x63: "c",
        0x64: "d",
        0x65: "e",
        0x66: "f",
        0x6F: "o",
    }

    # Build charstrings
    notdef_pen = T2CharStringPen(fc.width, None)
    draw_notdef(notdef_pen)

    space_pen = T2CharStringPen(fc.width, None)

    charstrings = {
        ".notdef": notdef_pen.getCharString(),
        "space": space_pen.getCharString(),
        "a": record_glyph(draw_a),
        "b": record_glyph(draw_b),
        "c": record_glyph(draw_c),
        "d": record_glyph(draw_d),
        "e": record_glyph(draw_e),
        "f": record_glyph(draw_f),
        "o": record_glyph(draw_o),
    }
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
    fb.setupHorizontalHeader(ascent=fc.ascent, descent=fc.descent)
    fb.setupNameTable(
        {
            "familyName": "OrbitonMono",
            "styleName": "Regular",
            "uniqueFontIdentifier": "OrbitonMono-Regular",
            "fullName": "OrbitonMono Regular",
            "version": "Version 1.000",
            "psName": "OrbitonMono-Regular",
        }
    )
    fb.setupOS2(
        sTypoAscender=fc.ascent,
        sTypoDescender=fc.descent,
        sTypoLineGap=0,
        usWinAscent=fc.ascent,
        usWinDescent=abs(fc.descent),
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
