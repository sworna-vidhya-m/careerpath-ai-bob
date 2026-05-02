# /review-pr

Run a focused pre-PR review on the current branch:

1. List all files changed vs main.
2. For each changed file, check:
   - Does it follow .bob/rules/project-rules.md?
   - Are there new public functions without docstrings?
   - Are there hardcoded secrets, API keys, or credentials?
   - Are there console.log or debug statements left behind?
3. Run the test suite if one exists; report failures.
4. Output a checklist of issues to fix before opening the PR.

Do not auto-fix. Only report.
