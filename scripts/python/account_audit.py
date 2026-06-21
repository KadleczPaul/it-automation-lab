#!/usr/bin/env python3
"""account_audit.py — audit de conturi dintr-un export AD (CSV).
Raporteaza conturi inactive si conturi active fara login recent (risc).
Usage: python3 account_audit.py [users.csv] [zile_prag]
"""
import csv, sys

def main():
    path = sys.argv[1] if len(sys.argv) > 1 else "data/users.csv"
    threshold = int(sys.argv[2]) if len(sys.argv) > 2 else 90

    rows = []
    with open(path, newline="") as f:
        for r in csv.DictReader(f):
            r["LastLogonDays"] = int(r["LastLogonDays"])
            r["Enabled"] = r["Enabled"] == "True"
            rows.append(r)

    # conturi ACTIVE dar inactive de >threshold zile = candidate de dezactivat
    stale = [r for r in rows if r["Enabled"] and r["LastLogonDays"] > threshold]
    disabled = [r for r in rows if not r["Enabled"]]

    print(f"Total conturi:            {len(rows)}")
    print(f"Conturi dezactivate:      {len(disabled)}")
    print(f"Active dar inactive >{threshold}z: {len(stale)}  <-- de revizuit\n")

    if stale:
        print(f"{'SamAccountName':<14}{'Department':<14}{'ZileFaraLogin':>13}")
        print("-" * 41)
        for r in sorted(stale, key=lambda x: -x["LastLogonDays"]):
            print(f"{r['SamAccountName']:<14}{r['Department']:<14}{r['LastLogonDays']:>13}")

    # scrie si un CSV de output (cum ai face intr-un raport real)
    with open("data/stale_accounts.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["SamAccountName","Name","Department","LastLogonDays"])
        w.writeheader()
        for r in stale:
            w.writerow({k: r[k] for k in w.fieldnames})
    print(f"\nRaport scris in data/stale_accounts.csv")

if __name__ == "__main__":
    main()
