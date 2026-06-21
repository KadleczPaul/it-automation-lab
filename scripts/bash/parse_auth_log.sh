#!/bin/bash
# parse_auth_log.sh — găsește IP-uri cu multe autentificări EȘUATE (posibil brute-force)
# Usage: ./parse_auth_log.sh <fisier_log> [prag]
set -euo pipefail

LOG="${1:-data/auth.log}"
THRESHOLD="${2:-15}"

if [[ ! -f "$LOG" ]]; then
  echo "Eroare: fisierul '$LOG' nu exista" >&2
  exit 1
fi

echo "== IP-uri cu >= $THRESHOLD autentificari esuate in $LOG =="
# grep liniile Failed -> extrage IP-ul (campul de dupa 'from') -> sorteaza si numara
grep "Failed password" "$LOG" \
  | grep -oE 'from [0-9.]+' \
  | awk '{print $2}' \
  | sort \
  | uniq -c \
  | sort -rn \
  | awk -v t="$THRESHOLD" '$1 >= t {printf "  %-15s %d incercari esuate\n", $2, $1}'

total_fail=$(grep -c "Failed password" "$LOG")
echo "Total autentificari esuate: $total_fail"
