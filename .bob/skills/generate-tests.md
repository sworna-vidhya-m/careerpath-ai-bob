# Skill: Generate Tests

For any function or component:

1. Cover the happy path first.
2. Cover edge cases: empty input, null, max boundaries, invalid types.
3. Cover error paths: what happens when a dependency throws.
4. Use the existing test framework. Check package.json before assuming.
5. Mock external services. No real API calls in tests.
6. Test names follow: "should <expected behavior> when <condition>"
