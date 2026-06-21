"""Generează date sample pentru lab: utilizatori (CSV) și auth log (text)."""
import csv, random, datetime as dt

random.seed(42)
depts = ["IT", "Engineering", "HR", "Finance", "Logistics", "Quality"]
first = ["Paul","Ana","Mihai","Elena","Andrei","Ioana","Radu","Maria","Vlad","Diana"]
last = ["Pop","Ionescu","Dragan","Munteanu","Stan","Barbu","Toma","Lazar"]

# users.csv — export tipic dintr-un Active Directory
with open("data/users.csv", "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["SamAccountName","Name","Department","Enabled","LastLogonDays"])
    for i in range(1, 61):
        fn, ln = random.choice(first), random.choice(last)
        sam = f"{fn[0].lower()}{ln.lower()}{i}"
        enabled = random.random() > 0.1          # ~10% disabled
        last_logon = random.choice([1,3,5,10,30,45,95,120,200])  # zile
        w.writerow([sam, f"{fn} {ln}", random.choice(depts), enabled, last_logon])

# auth.log — log de autentificare (succes/fail) stil Linux
ips = [f"10.20.{random.randint(1,5)}.{random.randint(2,254)}" for _ in range(15)]
with open("data/auth.log", "w") as f:
    base = dt.datetime(2026, 6, 21, 8, 0, 0)
    for i in range(400):
        t = base + dt.timedelta(seconds=i*37)
        ip = random.choice(ips)
        ok = random.random() > 0.25
        status = "Accepted" if ok else "Failed"
        user = random.choice(["paul","admin","root","ana","svc_backup"])
        f.write(f"{t:%b %d %H:%M:%S} srv01 sshd[{1000+i}]: {status} password for {user} from {ip} port {random.randint(40000,60000)} ssh2\n")

print("Generat: data/users.csv (60 utilizatori), data/auth.log (400 linii)")
