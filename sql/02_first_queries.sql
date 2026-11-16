-- Query 1: Row counts after importing CSV files.
SELECT 'departments' AS table_name, COUNT(*) AS rows_loaded FROM departments
UNION ALL SELECT 'employees', COUNT(*) FROM employees
UNION ALL SELECT 'attendance_monthly', COUNT(*) FROM attendance_monthly
UNION ALL SELECT 'training_records', COUNT(*) FROM training_records;

-- Query 2: Active employees by department on 31 October 2026.
-- Termination date is the first INACTIVE day.
SELECT d.department_name, COUNT(*) AS active_headcount
FROM employees e
JOIN departments d ON e.department_id = d.department_id
WHERE e.hire_date <= DATE '2026-10-31'
  AND (e.termination_date IS NULL OR e.termination_date > DATE '2026-10-31')
GROUP BY d.department_name
ORDER BY active_headcount DESC;

-- Query 3: Employee exits by month (only months with exits).
SELECT DATE_TRUNC('month', termination_date)::date AS exit_month,
       COUNT(*) AS employee_exits
FROM employees
WHERE termination_date IS NOT NULL
GROUP BY DATE_TRUNC('month', termination_date)
ORDER BY exit_month;

-- Query 4: Monthly absence percentage (sample attendance observations).
SELECT month_start,
       SUM(absence_days) AS absent_days,
       SUM(scheduled_days) AS scheduled_days,
       ROUND(100.0 * SUM(absence_days) / NULLIF(SUM(scheduled_days),0), 2) AS absence_pct
FROM attendance_monthly
GROUP BY month_start
ORDER BY month_start;

-- Query 5: Training score difference by course type.
-- Descriptive scores only; not evidence of causal training effectiveness.
SELECT training_type,
       COUNT(*) AS completions,
       ROUND(AVG(post_score-pre_score)::numeric,1) AS avg_score_change
FROM training_records
GROUP BY training_type
ORDER BY training_type;
