# Metric definitions and assumptions

All records are **synthetic**, generated for educational portfolio work (not Tesla or KWS data).

| Metric | Definition |
| --- | --- |
| Active headcount on date D | Employees with hire_date <= D and (termination_date is null or termination_date > D) |
| Monthly exits | Count of termination dates in the month; termination date means the first *inactive* day |
| Opening headcount | Active employees on the first day of a month |
| Closing headcount | Active employees on the last day of a month |
| Simplified monthly attrition (%) | 100 * exits / average(opening headcount, closing headcount) |
| Monthly absence (%) | 100 * sum(absence_days) / sum(scheduled_days) |
| Training score change | post_score - pre_score, in percentage points on synthetic assessments |

## Limitations

- **Not real HR observations.** All numbers are generated using a pseudorandom algorithm.
- Monthly attendance uses fixed 20 (full-time) or 12 (part-time) scheduled days even for partial employment months; absence rates are pedagogical, not payroll-grade.
- A training score improvement cannot be interpreted as a causal training effect.
- The project does not calculate time-to-hire, training completion rates, overtime or inferred employee risk scores.
- The status of a Power BI dashboard is **not built** as of this starter milestone.
