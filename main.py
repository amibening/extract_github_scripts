import os
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport

# from dotenv import load_dotenv

# Load environment variables from the config.env file
# load_dotenv('config.env')

# Fetch the GitHub access token from environment variables
github_token = "paste_GitHub_api_access_token_here"

if not github_token:
    raise ValueError("GITHUB_ACCESS_TOKEN not found. Make sure it is set in config.env.")

# Set up the GraphQL transport (API endpoint and headers)
transport = RequestsHTTPTransport(
    url="https://api.github.com/graphql",
    headers={"Authorization": f"Bearer {github_token}"},
    use_json=True,
)

# Initialize the client
client = Client(transport=transport, fetch_schema_from_transport=True)

# Define the GitHub search query
github_query = "NOT fork:true path:*.ak Aiken"

# Define the number of results to return per page (GitHub API limit is 1000 total)
num_results = 100  # GitHub GraphQL API allows a maximum of 100 results per call

# Try to read the cursor from a file to resume from the last known point
cursor_file = "pagination_cursor.txt"
start_cursor = None
if os.path.exists(cursor_file):
    with open(cursor_file, "r") as f:
        start_cursor = f.read().strip()  # Get the stored cursor


# Define the GraphQL query with pagination support
def build_query(cursor=None):
    cursor_str = f', after: "{cursor}"' if cursor else ""
    return gql(f"""
    {{
      search(query: "{github_query}", type: REPOSITORY, first: {num_results} {cursor_str}) {{
        edges {{
          node {{
            ... on Repository {{
              name
              owner {{
                login
              }}
              description
              isFork
              url
            }}
          }}
        }}
        pageInfo {{
          endCursor
          hasNextPage
        }}
      }}
    }}
    """)


# Function to fetch and paginate through results
def fetch_repositories(start_cursor_point=None):
    has_next_page = True
    cursor = start_cursor_point

    while has_next_page:
        query = build_query(cursor)
        result = client.execute(query)

        # Process the fetched repositories
        for repo in result['search']['edges']:
            repo_node = repo['node']
            print(f"Repository: {repo_node['name']}")
            print(f"Owner: {repo_node['owner']['login']}")
            print(f"Description: {repo_node.get('description', 'No description')}")
            print(f"Is Fork: {repo_node['isFork']}")
            print(f"URL: {repo_node['url']}\n")

        # Update pagination info
        page_info = result['search']['pageInfo']
        cursor = page_info['endCursor']
        has_next_page = page_info['hasNextPage']

        # Debug: Print cursor and pagination status
        print(f"Cursor: {cursor}")
        print(f"Has next page: {has_next_page}")

        # Save the current cursor to a file to resume later
        if cursor:  # Check if cursor is not None before writing
            with open(cursor_file, "w") as fi:
                fi.write(cursor)
        else:
            print("No more pages to paginate through.")

        # Break the loop if you reach 1000 records to respect the 1000 limit
        # GitHub limits queries to 1000 results.
        if has_next_page and len(result['search']['edges']) >= 1000:
            print("Reached 1000 records, stopping to comply with GitHub limits.")
            break


# Fetch the repositories starting from the last cursor (if any)
fetch_repositories(start_cursor)
