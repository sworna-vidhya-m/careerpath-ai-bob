# CareerPath AI — Project Rules for Bob

## Code style
- Match the existing formatting; do not reconfigure Prettier/ESLint
- Follow the import order already present in each file
- Keep functions under 50 lines where reasonable

## Documentation
- Every new public function gets a JSDoc/docstring
- Update README.md when user-facing behavior changes

## Security
- Never log API keys, tokens, or user PII
- Validate all user input on the server side
- Do not commit anything from .env or secrets/

## Testing
- New features require at least one test
- Do not delete or skip existing tests to make CI pass

## Workflow
- For tasks touching more than 3 files, use Plan mode before Code mode
- After code changes, run the test suite if one exists
- Reference skills in .bob/skills/ for repeatable workflows
