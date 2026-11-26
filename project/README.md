# Betty's Bird Boutique Customer Service Agent

The course project: a customer service agent for a bird store, built with Google's
Agent Development Kit (ADK) on Vertex AI. The agent answers questions about the store
and about birds with three tools, and it never takes orders:

1. **Product prices** from a Cloud SQL for MySQL database, through MCP Toolbox.
2. **Store information** (hours, history, staff) from PDF documents in a Vertex AI
   Search datastore.
3. **General bird questions** through Grounding with Google Search.

The step-by-step instructions, the assessment questions and the rubric are in the
classroom. This README covers the setup.

## Where to run it

Build and run the project in your **VM Lab**: in the classroom, open **Cloud Resources**,
start your lab, and open its VS Code workspace. The starter files are in
`project/starter`.

First complete the classroom's **ADK Setup and Deployment Guide** (on the "Access
Vocareum's VM Labs for GCP" page), including:

```bash
gcloud auth application-default login --no-launch-browser
```

That login is what lets your agent call Vertex AI with your lab account.

## Configure the environment

Create a `.env` file in the `project` folder (one level above `starter`, so it stays
out of the folder you submit):

```
GOOGLE_GENAI_USE_VERTEXAI=TRUE
GOOGLE_CLOUD_PROJECT=<your project ID>
GOOGLE_CLOUD_LOCATION=global

DATASTORE_PROJECT_ID=<your project ID>
DATASTORE_LOCATION=global
DATASTORE_ENGINE_ID=<your Vertex AI Search app ID>

TOOLBOX_URL=<the URL MCP Toolbox prints when it starts>

MYSQL_HOST=<your Cloud SQL instance's public IP address>
MYSQL_USER=<mysql user>
MYSQL_PASSWORD=<mysql password>
```

Use a `GOOGLE_CLOUD_LOCATION` of `global`: the Gemini models this project uses are
served there. In the course's lab projects, a regional location such as `us-central1`
answers `404 NOT_FOUND`.

## Dependencies

The VM Lab already has the libraries in `starter/requirements.txt`. On your own
machine, install them with:

```bash
pip install -r starter/requirements.txt
```

## Run MCP Toolbox

[Download the Toolbox server](https://mcp-toolbox.dev/documentation/introduction/#install-toolbox)
for your platform (Linux AMD64 in the VM Lab). Then, from the `starter` folder:

```bash
export $(grep -v '^#' ../.env | xargs)
/path/to/toolbox --tools-file tools.yaml --enable-api
```

`--enable-api` turns on the HTTP API that the `toolbox-core` Python client uses. Toolbox
0.31.0 and later turn it off by default, and without it the agent's tools fail to load
with `410 Gone`. An older Toolbox rejects the flag: download the current release. Leave
the server running in its own terminal.

## Run the agent

From the `project` folder, in a second terminal:

```bash
adk web
```

and choose `starter` in the previewer. On your own machine, open `http://127.0.0.1:8000`.
In the VM Lab, `adk web` runs inside the lab, so that address on your own computer does
not reach it. In another VS Code terminal, print your lab's address for it:

```bash
echo "$VSCODE_PROXY_URI" | sed 's/{{port}}/8000/'
```

It prints an address such as `https://vocproxy-2-23.us-west-2.vocareum.com/proxy/8000/`.
Open that address in a new browser tab with `dev-ui/` added at the end.

## Submit

Submit your `starter` folder as the classroom's **Submit Project** page describes, with
the screenshots the assessment asks for. Leave your `.env` file out: it holds your
database password.

## License
[License](../LICENSE.md)
