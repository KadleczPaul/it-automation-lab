<#
.SYNOPSIS
    Raport de spatiu pe disk; alerteaza daca un volum trece de un prag.
.EXAMPLE
    .\Get-DiskReport.ps1 -ThresholdPercent 85
#>
param([int]$ThresholdPercent = 85)

Get-CimInstance -ClassName Win32_LogicalDisk -Filter "DriveType=3" |
    ForEach-Object {
        $usedPct = [math]::Round(($_.Size - $_.FreeSpace) / $_.Size * 100, 1)
        [PSCustomObject]@{
            Drive      = $_.DeviceID
            UsedPct    = $usedPct
            FreeGB     = [math]::Round($_.FreeSpace / 1GB, 1)
            Alert      = if ($usedPct -ge $ThresholdPercent) { "ALERTA" } else { "ok" }
        }
    } | Format-Table -AutoSize
