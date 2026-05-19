import sqlite3
import json

DB_PATH = "applications.db"

def view_applications():
    conn = sqlite3.connect(DB_PATH)
    rows = conn.execute("""
        SELECT company, title, match_score, missing_skills,
               cover_letter, tailored_bullets, status, applied_date
        FROM applications
        ORDER BY match_score DESC
    """).fetchall()
    conn.close()

    if not rows:
        print("No applications found. Run main.py first!")
        return

    print(f"\nTotal applications: {len(rows)}\n")

    for i, row in enumerate(rows):
        company, title, score, missing, cover, bullets, status, date = row

        print("=" * 60)
        print(f"  [{i+1}] {title} at {company}")
        print(f"  Score  : {score}/100")
        print(f"  Status : {status}")
        print(f"  Date   : {date}")
        print(f"  Missing Skills: {', '.join(json.loads(missing))}")
        print()
        print("  COVER LETTER:")
        print(f"  {cover}")
        print()
        print("  TAILORED BULLETS:")
        for bullet in json.loads(bullets):
            print(f"    - {bullet}")
        print("=" * 60)
        print()

if __name__ == "__main__":
    view_applications()