#!/usr/bin/env python3

import sys
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

from db.connection import get_db_connection


BASE_DIR = Path(__file__).resolve().parent.parent
MIGRATIONS_DIR = BASE_DIR / "migrations"

LOCK_NAME = "tournamenthub_schema_migrations"


def create_schema_migrations_table(db):
    cursor = db.cursor()

    try:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS schema_migrations (
                version BIGINT UNSIGNED NOT NULL,
                filename VARCHAR(255) NOT NULL,
                applied_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

                PRIMARY KEY (version),
                UNIQUE KEY uq_schema_migrations_filename (filename)
            ) ENGINE=InnoDB
        """)

        db.commit()

    finally:
        cursor.close()


def get_applied_migrations(db):
    cursor = db.cursor(dictionary=True)

    try:
        cursor.execute("""
            SELECT version, filename
            FROM schema_migrations
            ORDER BY version
        """)

        return {
            row["version"]: row["filename"]
            for row in cursor.fetchall()
        }

    finally:
        cursor.close()


def get_migrations():
    migrations = []

    for path in MIGRATIONS_DIR.glob("*.sql"):
        try:
            version = int(path.name.split("_", 1)[0])
        except ValueError:
            continue

        migrations.append((version, path))

    migrations.sort(key=lambda x: x[0])

    return migrations


def run_migration(db, version, path):
    sql = path.read_text(encoding="utf-8").strip()

    if not sql:
        raise RuntimeError(f"Migration is empty: {path.name}")

    print(f"Applying {path.name}...")

    cursor = db.cursor()

    try:
        for statement in sql.split(";"):
            statement = statement.strip()

            if statement:
                cursor.execute(statement)

        cursor.execute("""
            INSERT INTO schema_migrations
                (version, filename)
            VALUES
                (%s, %s)
        """, (version, path.name))

        db.commit()

        print(f"✓ {path.name}")

    except Exception:
        db.rollback()
        raise

    finally:
        cursor.close()


def main():
    db = None

    try:
        db, _ = get_db_connection()

        create_schema_migrations_table(db)

        applied = get_applied_migrations(db)
        migrations = get_migrations()

        for version, path in migrations:

            if version in applied:
                continue

            run_migration(
                db,
                version,
                path
            )

        print("Database is up to date.")

        return 0

    except Exception as e:
        print(f"Migration failed: {e}")
        return 1

    finally:
        if db:
            db.close()


if __name__ == "__main__":
    sys.exit(main())