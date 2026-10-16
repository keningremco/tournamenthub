
#!/usr/bin/env python3
from pathlib import Path
import shutil
import sys

PROJECT_ROOT = Path(__file__).resolve().parent.parent
TEMPLATES_DIR = PROJECT_ROOT / "templates"
GENERATED_DIR = PROJECT_ROOT / "static" / "js" / "generated"


def main() -> int:
    if not TEMPLATES_DIR.is_dir():
        print(f"Fout: templates-map niet gevonden: {TEMPLATES_DIR}", file=sys.stderr)
        return 1

    sources = sorted(
        path for path in TEMPLATES_DIR.rglob("*.js")
        if path.is_file()
    )

    if GENERATED_DIR.exists():
        if not GENERATED_DIR.is_dir():
            print(f"Fout: dit pad is geen map: {GENERATED_DIR}", file=sys.stderr)
            return 1
        shutil.rmtree(GENERATED_DIR)

    GENERATED_DIR.mkdir(parents=True, exist_ok=True)

    for source in sources:
        destination = GENERATED_DIR / source.name

        # Lees de inhoud en voeg het oorspronkelijke pad toe als comment.
        content = source.read_text(encoding="utf-8")
        original_path = source.relative_to(PROJECT_ROOT).as_posix()

        header = f"// Source: {original_path}\n"
        destination.write_text(header + content, encoding="utf-8")

        print(f"Gekopieerd: {original_path} -> {destination.name}")

    print(f"\nKlaar: {len(sources)} JavaScript-bestand(en) verwerkt.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
