-- Advanced practice: simplified monthly attrition, Jan 2024 - Oct 2026.
-- Definition = exits / average(opening headcount, closing headcount) * 100.
-- Termination date marks the first INACTIVE day. Opening headcount is measured
-- on the first calendar day; closing headcount on the last calendar day.
WITH months AS (
    SELECT generate_series(DATE '2024-01-01',
                           DATE '2026-10-01',
                           INTERVAL '1 month')::date AS month_start
),
monthly AS (
    SELECT m.month_start,
        (SELECT COUNT(*) FROM employees e
         WHERE e.hire_date <= m.month_start
           AND (e.termination_date IS NULL OR e.termination_date > m.month_start)
        ) AS opening_headcount,
        (SELECT COUNT(*) FROM employees e
         WHERE e.hire_date <= (m.month_start + INTERVAL '1 month - 1 day')::date
           AND (e.termination_date IS NULL OR
                e.termination_date > (m.month_start + INTERVAL '1 month - 1 day')::date)
        ) AS closing_headcount,
        (SELECT COUNT(*) FROM employees e
         WHERE e.termination_date >= m.month_start
           AND e.termination_date < (m.month_start + INTERVAL '1 month')::date
        ) AS exits
    FROM months m
)
SELECT month_start, opening_headcount, closing_headcount, exits,
       ROUND(100.0 * exits /
             NULLIF((opening_headcount + closing_headcount) / 2.0, 0), 2
       ) AS simulated_attrition_pct
FROM monthly
ORDER BY month_start;
