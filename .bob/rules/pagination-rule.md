# UI Pagination Rule

When implementing or modifying any UI tab or list view that may display more than 10 records, follow these rules:

- **Default page size: 10 records per page.**
- Show pagination controls below the list: Previous / page number indicator (e.g. "Page 2 of 5") / Next.
- Disable Previous on page 1; disable Next on the last page.
- Show a small footer line below the controls indicating total records (e.g. "9 skills total · showing 1-10").
- Match the pagination pattern already used in the Employees tab in `static/index.html` — read it first to learn the existing pattern, then reuse the same approach.
- Filtering controls (dropdowns, search) reset pagination to page 1.
- This rule applies to all current and future UI tabs that display records.