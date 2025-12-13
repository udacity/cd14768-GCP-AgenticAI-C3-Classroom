
# Module 06 Exercise

## Environment

GOOGLE_GENAI_USE_VERTEXAI=TRUE
GOOGLE_CLOUD_PROJECT=<your project ID>
GOOGLE_CLOUD_LOCATION=us-central1

TOOLBOX_URL=http://127.0.0.1:5001

MYSQL_HOST=<your host ip address>
MYSQL_USER=<mysql user>
MYSQL_PASSWORD=<mysql password>


Make sure you replace <your project ID> with the ID for your project.

Using a LOCATION of us-central1 is usually the best bet in the United States,
but consider other cloud data center locations for elsewhere.

See below for the values that are needed for the TOOLBOX_URL and the
various MYSQL environment variables

## Additional Setup

### Setup Google Cloud SQL

If you do not already have an SQL instance to use:

1. In the Google Cloud Console, go to the "Cloud SQL" configuration. (Hint:
   You can search for it in the search bar.)
2. Select "Create Instance"
3. Choose MySQL
4. Select the Enterprise edition. **Not** the "Enterprise Plus" edition
5. Select Edition preset: Sandbox
6. Choose Database version: MySQL 8.0
7. Set the Instance ID
8. Set the root password
9. Choose the "us-central1" region with a Single zone. (You can choose
   another region, but it should be the one that most of your project runs in.)
10. Select Customize your instance
11. Change the Machine configuration to 1 vCPU
12. You can leave other settings alone and select the "Create instance" button.

Once the instance is created / updated, you can get the Public IP address
from the list of instances and enter it as the value for MYSQL_HOST in your
.env file.

You can then connect to the database server using the local mysql command
with something like:

```
mysql -h <ip_address> -u root -p 
```

You can then load in the database and files with a MySQL command
`\s docs/warehouse_database.sql`.

You then need to permit your user to the database with a MySQL command such as
`GRANT SELECT, INSERT, UPDATE ON 'warehouse'.* TO 'user_name'@'%'`

### Setup and run MCP Toolbox

See [here](https://googleapis.github.io/genai-toolbox/getting-started/introduction/)
for how to download the toolbox server for your platform.

To run the MCP server:
1. From the command line, change directories to where your tools.yaml file is
2. Make sure the MYSQL environment variables are exported in your current
   command line
    - If this is using bash, for example, you might do this as something like
      `export $(grep -v '^#' .env | xargs)`
3. Run `/path/to/toolbox --tools-file tools.yaml`
    - If you need to use another port, you can include a --port parameter

Update the TOOLBOX_URL in the .env file to specify the hostname (usually
localhost) and port the MCP Server is listening to.
