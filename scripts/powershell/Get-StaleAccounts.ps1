<#
.SYNOPSIS
    Auditeaza conturile dintr-un export CSV: gaseste conturi active fara login recent.
.DESCRIPTION
    Echivalentul PowerShell al account_audit.py. Pe un domeniu real ai folosi
    Get-ADUser in loc de Import-Csv (vezi blocul comentat de jos).
.EXAMPLE
    .\Get-StaleAccounts.ps1 -Path ..\..\data\users.csv -ThresholdDays 90
#>
param(
    [string]$Path = "..\..\data\users.csv",
    [int]$ThresholdDays = 90
)

if (-not (Test-Path $Path)) {
    Write-Error "Fisierul '$Path' nu exista"
    exit 1
}

$users = Import-Csv -Path $Path

$stale = $users | Where-Object {
    $_.Enabled -eq "True" -and [int]$_.LastLogonDays -gt $ThresholdDays
} | Sort-Object { [int]$_.LastLogonDays } -Descending

Write-Host "Total conturi:      $($users.Count)"
Write-Host "Active inactive >${ThresholdDays}z: $($stale.Count)  <-- de revizuit`n"

$stale | Select-Object SamAccountName, Department, LastLogonDays | Format-Table -AutoSize

# export raport (cum ai face intr-un task real)
$stale | Export-Csv -Path "..\..\data\stale_accounts_ps.csv" -NoTypeInformation
Write-Host "Raport scris in data\stale_accounts_ps.csv"

# --- VARIANTA REALA pe domeniu AD (necesita modulul ActiveDirectory) ---
# $cutoff = (Get-Date).AddDays(-$ThresholdDays)
# Get-ADUser -Filter {Enabled -eq $true -and LastLogonDate -lt $cutoff} `
#     -Properties LastLogonDate |
#     Select-Object Name, SamAccountName, LastLogonDate |
#     Export-Csv "stale_accounts.csv" -NoTypeInformation
