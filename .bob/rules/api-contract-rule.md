# API Contract Verification Rule

When writing frontend code (vanilla JS, React, or any client) that consumes a backend API, follow these rules to prevent runtime "undefined" errors:

## Before writing any frontend code that consumes an endpoint

1. **Curl the endpoint first** and inspect the actual JSON shape. Do not guess field names from memory or schemas.
2. **Match field names exactly** as they appear in the response. Watch for:
   - Singular vs plural (`recommendation` vs `recommendations`)
   - Suffix conventions (`readiness` vs `readiness_label` vs `readinessLevel`)
   - snake_case vs camelCase mismatches
3. **Cross-check Pydantic schema names with serialized JSON output** — Pydantic may rename fields via `alias`, `serialization_alias`, or `Field(...)` configurations.

## When rendering optional or nullable fields

4. **Always guard against undefined/null** before calling string methods:
   - Wrong: `rec.field.toLowerCase()`
   - Right: `(rec.field || '').toLowerCase()` or `rec.field?.toLowerCase() ?? ''`
5. **Provide visible fallbacks** for nullable fields (e.g. `to_band` shows "—" or "TBD" when null), not silent empty strings that confuse users.

## When the contract changes

6. If a backend response shape changes, the corresponding frontend code must be updated in the same task. Do not leave stale field names.
7. Update any rendering logic that depends on the old shape, including conditional class names and label text.

## Testing

8. After any frontend change that depends on an API response, hit the endpoint via curl and visually confirm the data renders correctly in the browser. Do not rely on tests alone — frontend bugs are runtime bugs.

This rule applies to all current and future frontend code in this project. Reference this rule when writing new UI features that consume backend endpoints.