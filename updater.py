import time
import mysql.connector
from datetime import datetime
from dotenv import load_dotenv
import os

load_dotenv()

def get_db_connection():
    db = mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME")
    )

    cursor = db.cursor(dictionary=True)

    return db, cursor

def update_game_statuses():
    db, cursor = get_db_connection()

    try:
        now = datetime.now()

        cursor.execute("""
            SELECT id, start_time, roundId, status
            FROM games
            WHERE status = 'scheduled'
            ORDER BY start_time ASC
        """)

        games = cursor.fetchall()

        for game in games:
            if game["start_time"] is not None and game["start_time"] <= now:
                cursor.execute("""
                    UPDATE games
                    SET status = 'in_progress'
                    WHERE id = %s
                      AND status = 'scheduled'
                """, (game["id"],))

                print(
                    f"[{now.strftime('%Y-%m-%d %H:%M:%S')}] "
                    f"Game {game['id']} -> in_progress"
                )
                
        db.commit()

    except Exception as e:
        db.rollback()
        print(f"Fout bij updaten game status: {e}")

    finally:
        cursor.close()
        db.close()


def main():
    while True:
        try:
            update_game_statuses()
        except Exception as e:
            print(f"Fout: {e}")

        time.sleep(10)


if __name__ == "__main__":
    main()