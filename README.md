# People Analytics Intelligence Dashboard | SQL + Power BI

**Status: Milestone 1 — working synthetic dataset and PostgreSQL query scripts. The Power BI dashboard has NOT been built.**

This learning portfolio project uses **100% fictional employee records** for a hypothetical manufacturing company. It demonstrates early-stage SQL analytics for HR reporting. Nothing here is Tesla, KWS, or real employee data.

## Business questions

1. How many employees are active by department at the reporting date?
2. When are employee exits occurring?
3. How do simulated absence rates vary by month?
4. How do pre/post training assessment scores compare?
5. How can monthly employee attrition be calculated transparently?

## Repository layout

- `data/`: four generated synthetic CSV tables
- `src/generate_data.py`: deterministic, standard-library-only data generator
- `sql/01_create_tables.sql`: PostgreSQL schema and constraints
- `sql/02_first_queries.sql`: introductory queries (JOIN, GROUP BY, aggregation)
- `sql/03_monthly_attrition.sql`: practice query with CTEs, date series and rates
- `tests/test_dataset.py`: checks for data shape, date consistency and valid references
- `docs/metric_definitions.md`: business definitions and limitations
- `docs/progress_log.md`: milestones, checked only when personally verified
- `visuals/`: placeholder for future Power BI dashboard screenshots

## Reproduce the data (Python 3)

```bash
python src/generate_data.py
python -m unittest discover -s tests -v
```

The Python generator uses a fixed seed and can recreate all four CSVs. No external Python packages are required.

## Load into PostgreSQL (pgAdmin)

1. Install PostgreSQL and pgAdmin; create a **new empty database** called `people_analytics`.
2. Open Query Tool for the new database and run `sql/01_create_tables.sql`.
3. In pgAdmin, import the CSV files with the Import/Export Data dialog: **Import**, **CSV**, **Header = Yes**, **UTF-8**.
4. **Import in this order:** departments, employees, attendance_monthly, training_records (foreign keys).
5. Run `sql/02_first_queries.sql`, then `sql/03_monthly_attrition.sql`.
6. Compare the row-count query results with the CSVs; inspect actual SQL results before claiming any findings.

**Re-import warning:** create tables/import into a new empty database or clear tables before re-importing; importing twice will create duplicate-key errors.

## Next milestones

- Run SQL locally, interpret results, and add an independent query.
- Connect PostgreSQL to Power BI Desktop.
- Build Workforce Overview, Attrition, Attendance and Training pages.
- Add `.pbix`, screenshots, data-model notes and a short insight report after testing.

## Data ethics & limitations

All data is **synthetic and randomly simulated**; observed patterns cannot represent real-world employee behavior. Monthly attendance figures use simplified scheduled days even in partial employment months. Training score change is descriptive and **does not prove** training effectiveness. Termination date is defined as the **first inactive day**. Dashboard and findings are not yet completed.

**Project status:** This repository contains a prepared learning scaffold. SQL results, dashboard visuals and business findings will be added only after being run and verified.
