import os
from pathlib import Path

from PIL import Image


INPUT_FILE = "icon.png"
OUTPUT_FOLDER = "output"

PNG_TARGETS = [
    (32, "32x32.png"),
    (128, "128x128.png"),
    (256, "128x128@2x.png"),

    # Windows Store / tile assets
    (30, "Square30x30Logo.png"),
    (44, "Square44x44Logo.png"),
    (71, "Square71x71Logo.png"),
    (89, "Square89x89Logo.png"),
    (107, "Square107x107Logo.png"),
    (142, "Square142x142Logo.png"),
    (150, "Square150x150Logo.png"),
    (284, "Square284x284Logo.png"),
    (310, "Square310x310Logo.png"),
    (50, "StoreLogo.png"),
]


ICO_SIZES = [
    16,
    20,
    24,
    32,
    40,
    48,
    64,
    96,
    128,
    256,
]


ICNS_SIZES = [
    16,
    32,
    64,
    128,
    256,
    512,
    1024,
]

# ----------------------Helper---------------------- #

def resize_icon(source: Image.Image, size: int) -> Image.Image:
    """
    Resize the icon using high-quality Lanczos resampling.

    RGBA is used so transparency is preserved.
    """
    return source.resize(
        (size, size),
        Image.Resampling.LANCZOS
    ).convert("RGBA")


def save_png(source: Image.Image, size: int, path: Path):
    """
    Create a high-quality PNG icon.
    """
    icon = resize_icon(source, size)

    icon.save(
        path,
        format="PNG",
        optimize=True
    )


# -----------------Main conversion------------------ #

def convert_icons(
    input_file: str = INPUT_FILE,
    output_folder: str = OUTPUT_FOLDER
):
    input_path = Path(input_file)
    output_path = Path(output_folder)

    # 1. Verify input

    if not input_path.exists():
        print(f"ERROR: {input_file} was not found.")
        return

    output_path.mkdir(parents=True, exist_ok=True)

    print(f"Input : {input_path}")
    print(f"Output: {output_path}")
    print()

    # 2. Load source icon

    print("Loading source icon...")

    source = Image.open(input_path).convert("RGBA")

    print(f"Source size: {source.width}x{source.height}")

    if source.width < 1024 or source.height < 1024:
        print(
            "WARNING: Your source icon is smaller than 1024x1024.\n"
            "For best results, use a 1024x1024 or larger source icon."
        )

    print()

    # 3. Generate PNG assets

    print("Generating PNG assets...")

    for size, filename in PNG_TARGETS:
        destination = output_path / filename

        save_png(
            source,
            size,
            destination
        )

        print(f"  Generated {filename} ({size}x{size})")

    print()

    # 4. Generate MULTI-RESOLUTION Windows ICO

    print("Generating Windows icon.ico...")

    ico_images = [
        resize_icon(source, size)
        for size in ICO_SIZES
    ]

    ico_path = output_path / "icon.ico"

    # Pillow stores all supplied sizes inside ONE ICO file.
    #
    # This is the important part:
    # Windows can now choose the appropriate resolution instead
    # of scaling one 128x128 image everywhere.
    ico_images[-1].save(
        ico_path,
        format="ICO",
        sizes=[(img.width, img.height) for img in ico_images],
    )

    print(
        f"  Generated icon.ico "
        f"({', '.join(f'{s}x{s}' for s in ICO_SIZES)})"
    )

    print()

    # 5. Generate Apple ICNS

    print("Generating Apple icon.icns...")

    icns_images = [
        resize_icon(source, size)
        for size in ICNS_SIZES
    ]

    icns_path = output_path / "icon.icns"

    # Pillow's ICNS writer creates the required representations.
    icns_images[-1].save(
        icns_path,
        format="ICNS",
        sizes=[(img.width, img.height) for img in icns_images],
    )

    print(
        f"  Generated icon.icns "
        f"({', '.join(f'{s}x{s}' for s in ICNS_SIZES)})"
    )

    print()

    # 6. Generate master Tauri icon.png

    print("Generating icon.png...")

    final_icon = resize_icon(source, 512)

    final_icon.save(
        output_path / "icon.png",
        format="PNG",
        optimize=True
    )

    print("  Generated icon.png (512x512)")

    # Done

    print()
    print("=" * 60)
    print("DONE")
    print("=" * 60)
    print(f"Icons are located in: {output_path.resolve()}")


# ---------------------------------------------------------
# Entry point
# ---------------------------------------------------------

if __name__ == "__main__":
    convert_icons()

