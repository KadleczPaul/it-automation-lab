#!/usr/bin/env python3
"""run_sql.py — creeaza un DB SQLite din users.csv si ruleaza un fisier .sql."""
import csv, sqlite3, sys

def main():
    sql_file = sys.argv[1] if len(sys.argv) > 1 else "sql/queries/access_audit.sql"
    con = sqlite3.connect(":memory:")
    cur = con.cursor()

    # 1. schema
    with open("sql/schema.sql") as f:
        cur.executescript(f.read())

    # 2. load date din CSV
    with open("data/users.csv", newline="") as f:
        rows = [(r["SamAccountName"], r["Name"], r["Department"],
                 1 if r["Enabled"]=="True" else 0, int(r["LastLogonDays"]))
                for r in csv.DictReader(f)]
    cur.executemany("INSERT INTO users VALUES (?,?,?,?,?)", rows)
    con.commit()

    # 3. ruleaza interogarea si afiseaza ca tabel
    with open(sql_file) as f:
        query = f.read()
    cur.execute(query)
    cols = [d[0] for d in cur.description]
    print(" | ".join(f"{c:<14}" for c in cols))
    print("-" * (17 * len(cols)))
    for row in cur.fetchall():
        print(" | ".join(f"{str(v):<14}" for v in row))

if __name__ == "__main__":
    main()
