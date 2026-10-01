from pathlib import Path


# ============================================================
# CSS BUILD CONFIG
# ============================================================

CSS_DIR = Path("static/css")
STYLE_FILE = CSS_DIR / "style.css"

CSS_ORDER = [
    'variables.css',
    "base.css"
]


def build_style_css():
    """
    Bouwt style.css opnieuw op.

    Volgorde:
    1. Bestanden uit CSS_ORDER
    2. Alle overige .css bestanden
    3. style.css wordt nooit als bron gebruikt
    """
    print('doet iets')
    CSS_DIR.mkdir(parents=True, exist_ok=True)

    # Alle CSS-bestanden ophalen behalve style.css
    all_css_files = {
        file.name: file
        for file in CSS_DIR.glob("*.css")
        if file.name != STYLE_FILE.name
    }

    ordered_files = []
    used_files = set()

    # --------------------------------------------------------
    # 1. Eerst de bestanden uit CSS_ORDER
    # --------------------------------------------------------

    for filename in CSS_ORDER:
        css_file = all_css_files.get(filename)

        if css_file is None:
            continue

        ordered_files.append(css_file)
        used_files.add(filename)

    # --------------------------------------------------------
    # 2. Daarna alle overige CSS-bestanden
    # --------------------------------------------------------

    remaining_files = sorted(
        file
        for filename, file in all_css_files.items()
        if filename not in used_files
    )

    ordered_files.extend(remaining_files)

    # --------------------------------------------------------
    # 3. style.css volledig opnieuw schrijven
    # --------------------------------------------------------

    with STYLE_FILE.open("w", encoding="utf-8") as output:

        for css_file in ordered_files:

            output.write(
                f"\n"
                f"/* ==================================================\n"
                f"   {css_file.name}\n"
                f"   ================================================== */\n\n"
            )

            output.write(
                css_file.read_text(encoding="utf-8")
            )

            output.write("\n\n")


