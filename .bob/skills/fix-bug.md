# Skill: Debug and Fix

When asked to fix a bug:

1. Reproduce: ask for exact steps or error message if not provided.
2. Locate root cause by reading the failing code path end-to-end. Do not patch
   symptoms.
3. Explain the root cause in 2-3 sentences before changing code.
4. Apply the minimal fix.
5. Add a regression test if test infrastructure exists.
6. Summarize: what was broken, what you changed, why it works now.

Never:
- Suppress errors with empty catch blocks
- Comment out failing tests
- Add console.log statements as the "fix"
