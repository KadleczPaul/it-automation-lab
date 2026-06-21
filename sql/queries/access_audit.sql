-- access_audit.sql — câte conturi active/inactive pe departament
SELECT
    department,
    COUNT(*)                                   AS total,
    SUM(CASE WHEN enabled = 1 THEN 1 ELSE 0 END) AS active,
    SUM(CASE WHEN enabled = 1 AND last_logon_days > 90
             THEN 1 ELSE 0 END)                AS stale_active
FROM users
GROUP BY department
ORDER BY stale_active DESC, department;
