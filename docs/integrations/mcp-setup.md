# MCP Setup Documentation

This document describes the Model Context Protocol (MCP) servers configured for Claude Code.

## Installed MCP Servers

### 1. Puppeteer MCP Server
- **Purpose**: Browser automation and web scraping
- **Package**: `@modelcontextprotocol/server-puppeteer`
- **Binary**: `/Users/brianhardin/.nvm/versions/node/v22.17.0/bin/mcp-server-puppeteer`
- **Configuration**: No additional environment variables required

**Capabilities:**
- Take screenshots of web pages
- Extract text content from websites
- Automate browser interactions
- Test web applications
- Scrape dynamic content

### 2. Context7 MCP Server
- **Purpose**: Vector database and semantic search
- **Package**: `@upstash/context7-mcp`
- **Binary**: `/Users/brianhardin/.nvm/versions/node/v22.17.0/bin/context7-mcp`
- **Configuration**: Requires `CONTEXT7_API_KEY` environment variable

**Capabilities:**
- Store and retrieve documents with semantic search
- Vector embeddings for text similarity
- Context-aware information retrieval
- Document management and organization

## Configuration File

Location: `~/.config/claude-code/claude_desktop_config.json`

```json
{
  "mcpServers": {
    "context7": {
      "command": "/Users/brianhardin/.nvm/versions/node/v22.17.0/bin/context7-mcp",
      "args": [],
      "env": {
        "CONTEXT7_API_KEY": ""
      }
    },
    "puppeteer": {
      "command": "/Users/brianhardin/.nvm/versions/node/v22.17.0/bin/mcp-server-puppeteer",
      "args": [],
      "env": {}
    }
  }
}
```

## Setup Instructions

### Context7 API Key
To use Context7, you need to:
1. Sign up for a Context7 account at [context7.io](https://context7.io)
2. Get your API key from the dashboard
3. Add it to the configuration file or set as an environment variable

### Restart Claude Code
After making configuration changes, restart Claude Code for the MCP servers to be loaded.

## Usage Examples

### Puppeteer
- "Take a screenshot of my website at localhost:8000"
- "Extract all links from this webpage"
- "Test if my contact form works"

### Context7
- "Store this document in Context7"
- "Search for information about Python frameworks"
- "Find similar content to this text"

## Troubleshooting

### Common Issues
1. **MCP servers not loading**: Restart Claude Code
2. **Context7 authentication**: Verify API key is correct
3. **Puppeteer browser issues**: Ensure system has browser dependencies

### Verification
Check if MCP servers are working by looking for them in Claude Code's available tools after restart.

## Maintenance

- Keep packages updated: `npm update -g @upstash/context7-mcp @modelcontextprotocol/server-puppeteer`
- Monitor for new MCP server releases
- Backup configuration file when making changes
