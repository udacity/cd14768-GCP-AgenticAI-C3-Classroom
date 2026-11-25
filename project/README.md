# Betty's Bird Shop Agent

This Google ADK project provides a bird-shop customer service agent using:

- MCP Toolbox and MySQL product data
- Vertex AI Search for indexed store documents
- A grounded Google Search sub-agent
- Short-term in-memory sessions

## Setup

1. Load `project/starter/docs/betty_db.sql` into a MySQL database named `betty`.
2. Install dependencies:

   ```bash
   python -m pip install -r project/starter/requirements.txt
   ```

3. Copy `project/starter/.env-sample` to `.env` and replace placeholders.
4. Start MCP Toolbox:

   ```bash
   ./toolbox --tools-file project/starter/tools.yaml --port 5000
   ```

5. Start ADK:

   ```bash
   python -m google.adk.cli web project --host 127.0.0.1 --port 8005
   ```

## Environment Variables

- `GOOGLE_GENAI_USE_VERTEXAI`
- `GOOGLE_CLOUD_PROJECT`
- `GOOGLE_CLOUD_LOCATION`
- `GOOGLE_GENAI_MODEL` (verify availability; default: `gemini-3.8-flash`)
- `TOOLBOX_URL`
- `MYSQL_HOST`
- `MYSQL_PORT`
- `MYSQL_USER`
- `MYSQL_PASSWORD`
- `DATASTORE_PROJECT_ID`
- `DATASTORE_LOCATION`
- `DATASTORE_ENGINE_ID`

Never commit `.env` or credentials.

## Testing

```bash
python -m compileall -q project/starter
python -c "import project.starter"
```

In one ADK session, test the following requests:

1. Ask for the price of `Bird Seed Mix` and verify `get_product_price` returns
   the database result.
2. Ask for an unknown product and verify the agent reports no matching result.
3. Ask "What are the store's working hours?" and "Who is Betty?" and verify
   each invokes `datastore_search_tool`.
4. Ask a current bird-care question and verify `search_agent_tool` uses
   grounded Google Search and shows its sources.

Expand the relevant request/response tool events and keep the session ID
visible when capturing evidence. Save genuine ADK screenshots as PNG/JPEG
files in `screenshots/`. Include evidence for both found and not-found product
lookups, both datastore questions, and grounded web search.
