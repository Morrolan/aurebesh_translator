#!/usr/bin/env python3
"""
Generate the app icon assets (icons/icon.png, icons/icon.ico) from the
Aurebesh OTF font, using the same colour palette as the GUI.
Run: python tools/generate_icon.py
"""

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).parent.parent
FONT_PATH = ROOT / "fonts" / "Aurebesh.otf"
OUT_DIR = ROOT / "icons"

BG     = (6, 6, 15)      # matches gui.py BG
BORDER = (255, 215, 0)   # matches gui.py ACCENT
GLYPH  = (255, 215, 0)   # matches gui.py GLYPH_COLOR

SIZE = 512
BORDER_WIDTH = 14
CORNER_RADIUS = 90
GLYPH_CHAR = "A"  # Aurek
ICO_SIZES = (16, 24, 32, 48, 64, 128, 256)


def render_base(size: int) -> Image.Image:
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    scale = size / SIZE
    radius = CORNER_RADIUS * scale
    border = max(1, round(BORDER_WIDTH * scale))

    draw.rounded_rectangle(
        (0, 0, size - 1, size - 1), radius=radius, fill=BG, outline=BORDER, width=border,
    )

    font_size = round(size * 0.62)
    font = ImageFont.truetype(str(FONT_PATH), font_size)
    bbox = font.getbbox(GLYPH_CHAR)
    gw, gh = bbox[2] - bbox[0], bbox[3] - bbox[1]
    pos = ((size - gw) / 2 - bbox[0], (size - gh) / 2 - bbox[1])
    draw.text(pos, GLYPH_CHAR, font=font, fill=GLYPH)

    return img


def write_icons(out_dir: Path = OUT_DIR) -> tuple[Path, Path]:
    """Render and write icon.png + icon.ico into out_dir; returns their paths."""
    out_dir.mkdir(parents=True, exist_ok=True)
    png_path = out_dir / "icon.png"
    ico_path = out_dir / "icon.ico"

    icon_png = render_base(SIZE)
    icon_png.save(png_path)
    icon_png.save(ico_path, sizes=[(s, s) for s in ICO_SIZES])
    return png_path, ico_path


def main() -> None:
    png_path, ico_path = write_icons()
    print(f"Wrote {png_path} and {ico_path}")


if __name__ == "__main__":
    main()
