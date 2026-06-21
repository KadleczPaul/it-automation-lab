# IT Automation Lab

Repo de practica care imita un repo intern de automatizari IT/Ops.
Contine scripturi de audit de conturi si securitate in 4 tehnologii:
PowerShell, Bash, Python si SQL.

## Structura
```
scripts/
  powershell/  Get-StaleAccounts.ps1, Get-DiskReport.ps1
  bash/        parse_auth_log.sh
  python/      account_audit.py, run_sql.py
sql/
  schema.sql
  queries/access_audit.sql
data/          date sample (users.csv, auth.log) + generator
```

## Setup
```bash
git clone <url-repo>
cd it-automation-lab
python3 data/generate_sample_data.py   # (re)genereaza datele sample
```

## Cum rulezi fiecare script

### Bash — detectie de brute-force in log
```bash
./scripts/bash/parse_auth_log.sh data/auth.log 5
```

### Python — audit de conturi inactive
```bash
python3 scripts/python/account_audit.py data/users.csv 90
```

### SQL — audit pe departament
```bash
python3 scripts/python/run_sql.py sql/queries/access_audit.sql
```

### PowerShell (pe Windows)
```powershell
cd scripts\powershell
.\Get-StaleAccounts.ps1 -Path ..\..\data\users.csv -ThresholdDays 90
.\Get-DiskReport.ps1 -ThresholdPercent 85
```
> Daca primesti eroare de execution policy:
> `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass`

## Workflow de contributie
1. `git checkout -b feature/numele-tau`
2. modifici / adaugi un script
3. `git add` + `git commit -m "mesaj clar"`
4. `git push` si deschizi un Pull Request

Primul meu commit de test - Paul
