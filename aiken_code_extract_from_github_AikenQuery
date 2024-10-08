from github import Github
import requests
import json

# Replace 'your_github_token' with your actual GitHub personal access token
GITHUB_TOKEN = "GitHub personal access token"

# Initialize GitHub object using PyGithub
g = Github(GITHUB_TOKEN)


# Code only searches files with .ak extension
# Use the above as a search query for results

def search_files_with_extension(extension_in, repo_name_in=None):
    query = f'extension:{extension_in}'
    result = g.search_code(query)
    return result


def download_and_format_files(files_in, limit_in):
    data_in = []
    count = 0
    for file in files_in:
        count = count + 1
        if count > limit_in:
            print(f"Output Limited to  : {limit_in}")
            print(f"******************************************************")
            break

        file_url = file.download_url
        file_name = file.path.split("/")[-1]

        response = requests.get(file_url)
        if response.status_code == 200:
            code_content = response.text
            description = f"Code extracted from {file_name} located in {file.repository.full_name} repository."

            # Append to data list
            data_in.append({
                "instruction": description,
                "input": "",
                "output": code_content
            })
            print(f"Processed: {file_name}")
        else:
            print(f"Failed to download: {file_name}")

    return data_in


def save_to_json(data_out, output_file2):
    with open(output_file2, 'w') as json_file:
        json.dump(data_out, json_file, indent=4)
    print(f"Data saved to {output_file2}")


if __name__ == "__main__":
    limit_search_output = 100

    # Search for files with .ak extension in all public repositories
    extension = "ak design"
    repo_name = None  # Replace with 'username/repository' to search in a specific repo

    files = search_files_with_extension(extension, repo_name)
    print(f"Found {files.totalCount} files with .{extension} extension")
    print(f"Note Output Limited to  : {limit_search_output} this can be amened in the code")
    print(f"************************************************************")

    data = download_and_format_files(files, limit_search_output)

    # Define the output JSON file
    output_file = "aiken_code_data_withAikenQuery_instruction_input_output.json"
    save_to_json(data, output_file)
