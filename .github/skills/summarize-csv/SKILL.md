---
name: summarize-csv
description: 'Summarize the synthetic sales CSV by region, explain the regional-total average, and verify behavior with the starter app and tests. Use for questions or tasks about this workshop CSV report.'
---

# Summarize the workshop sales CSV

## Scope and rules

- Work only on `ws-part1-github-copilot/labs/starter` for application files.
- Read its `README.md` before working; it is the source of the business rules.
- Use the README's rules for required CSV columns, region names, amounts, regional totals, average per region, top-region tie-breaking, empty input, validation, and the optional filter. Some rules are intentionally implemented in later labs.
- Do not read presenter answers or edit Part 2.
- Do not silently fix unrelated code. Explain unrelated issues separately and change them only if asked.

## Procedure

1. From the fork root, inspect the worktree read-only, then enter `ws-part1-github-copilot/labs/starter`.
2. Use the local `.venv` interpreter. Run `python summarize.py data/sales.csv` and `python -m pytest -q` from the starter folder. Do not install application dependencies.
3. Explain the output against the input and README. The average is the arithmetic mean of regional totals, not the mean of individual rows. For `data/sales.csv`, the totals are East 150, West 250, and North 75; the average is `(150 + 250 + 75) / 3`, approximately `158.33`.
4. If the report or tests expose a defect, describe it and its scope. Make only changes needed for the user's request; preserve unfinished behavior assigned to later labs.
