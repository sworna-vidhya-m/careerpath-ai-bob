# Skill: Build a Local MCP Server for CareerPath AI

When asked to create or extend the local MCP server, follow this exactly:

## Location and structure

Create the server under `mcp/careerpath-mcp/` with these files:

- `package.json` — type: "module", main: "server.js", dependency on
  `@modelcontextprotocol/sdk`, and a `start` script
- `server.js` — the MCP server using StdioServerTransport
- `README.md` — how to run and how to register with Bob

## Tools to expose

The server must expose at minimum these three tools (adjust names/shapes
to match the actual data structures in the CareerPath AI codebase):

1. `get_career_paths` — returns the list of supported career tracks
2. `validate_user_profile` — takes a user profile object, returns
   `{ valid: boolean, errors: string[] }`
3. `get_skill_gap` — takes `{ currentSkills, targetCareer }`, returns
   the list of missing skills

Before implementing, read the existing app code to find the real shapes
of "career path", "user profile", and "skill" — do not invent shapes.

## Implementation rules

- Use ESM imports, not CommonJS
- Each tool needs: name, description, inputSchema (JSON Schema), and
  a handler function
- Handlers must validate input and return MCP-compliant responses:
  `{ content: [{ type: "text", text: "..." }] }`
- Errors are returned as `{ content: [...], isError: true }`, not thrown
- No network calls; read from local data/modules only

## Testing

Add `mcp/careerpath-mcp/server.test.js` with one test per tool covering
the happy path and one invalid-input case.

## Registration instructions in README

The README must tell the user how to register the server in Bob IDE:
Settings → MCP → add a project-level server with command `node` and
args `mcp/careerpath-mcp/server.js`.
