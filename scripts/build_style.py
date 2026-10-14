from pathlib import Path


# ============================================================
# CSS BUILD CONFIG
# ============================================================

CSS_DIR = Path("static/css")
STYLE_FILE = CSS_DIR / "style.css"
TEMPLATES_DIR = Path("templates")

CSS_ORDER = [
    "variables.css",
    "base.css",
]

# True  = print alle gevonden CSS-bestanden en hun inhoud
# False = geen uitgebreide terminal-output
PRINT_CSS_FILES = False


def build_style_css():
    """
    Bouwt style.css opnieuw op.

    Volgorde:
    1. Bestanden uit CSS_ORDER in static/css
    2. Alle overige CSS-bestanden in static/css
    3. Alle CSS-bestanden in templates en submappen

    style.css wordt nooit als bron gebruikt.
    """

    CSS_DIR.mkdir(parents=True, exist_ok=True)

    ordered_files = []
    used_files = set()

    # ========================================================
    # 1. CSS-BESTANDEN UIT static/css OPHALEN
    # ========================================================

    all_css_files = {
        file.name: file
        for file in CSS_DIR.glob("*.css")
        if file.name != STYLE_FILE.name
    }

    # Eerst de bestanden uit CSS_ORDER
    for filename in CSS_ORDER:
        css_file = all_css_files.get(filename)

        if css_file is None:
            continue

        ordered_files.append(
            (css_file.name, css_file)
        )
        used_files.add(filename)

    # Daarna de overige bestanden alfabetisch
    remaining_files = sorted(
        (
            file
            for filename, file in all_css_files.items()
            if filename not in used_files
        ),
        key=lambda file: file.name.lower(),
    )

    for css_file in remaining_files:
        ordered_files.append(
            (css_file.name, css_file)
        )

    # ========================================================
    # 2. CSS-BESTANDEN UIT templates EN SUBMAPPEN OPHALEN
    # ========================================================

    if TEMPLATES_DIR.exists():

        template_css_files = sorted(
            TEMPLATES_DIR.rglob("*.css"),
            key=lambda file: file.as_posix().lower(),
        )

        for css_file in template_css_files:
            # Het relatieve pad maakt duidelijk uit welke map
            # het bestand afkomstig is.
            relative_path = css_file.relative_to(
                TEMPLATES_DIR
            ).as_posix()

            ordered_files.append(
                (f"templates/{relative_path}", css_file)
            )

    # ========================================================
    # 3. style.css VOLLEDIG OPNIEUW SCHRIJVEN
    # ========================================================

    with STYLE_FILE.open("w", encoding="utf-8") as output:

        for filename, css_file in ordered_files:

            content = css_file.read_text(
                encoding="utf-8"
            )

            # Bestandsnaam als commentaar in style.css
            output.write(
                "\n"
                "/* ==================================================\n"
                f"   {filename}\n"
                "   ================================================== */\n\n"
            )

            output.write(content)
            output.write("\n\n")

            # Optionele terminal-output
            if PRINT_CSS_FILES:
                print("\n" + "=" * 70)
                print(f"CSS-BESTAND: {css_file}")
                print("=" * 70)
                print(content)

    # ========================================================
    # 4. RESULTAAT TONEN
    # ========================================================

    if PRINT_CSS_FILES:
        print("\n" + "=" * 70)
        print("CSS BUILD VOLTOOID")
        print(f"Aantal verwerkte bestanden: {len(ordered_files)}")
        print(f"Samengevoegd bestand: {STYLE_FILE}")
        print("=" * 70)

    return STYLE_FILE


if __name__ == "__main__":
    build_style_css()