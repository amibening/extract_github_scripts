import os
import json


def combine_json_files(input_directory, output_file):
    combined_data = []

    # Loop through all files in the directory
    for filename in os.listdir(input_directory):
        if filename.endswith('.json'):
            file_path = os.path.join(input_directory, filename)

            # Open and read each JSON file
            with open(file_path, 'r') as json_file:
                try:
                    data = json.load(json_file)

                    # Check if the file contains a list and extend it, otherwise just append the object
                    if isinstance(data, list):
                        combined_data.extend(data)  # Add elements from the list, not the list itself
                    else:
                        combined_data.append(data)  # Add the single object

                except json.JSONDecodeError as e:
                    print(f"Error decoding {filename}: {e}")

    # Write combined data to the output file with a single pair of square brackets
    with open(output_file, 'w') as output_json_file:
        json.dump(combined_data, output_json_file, indent=4)

    print(f"Combined {len(combined_data)} JSON objects into {output_file}")


def main():
    # Argument for setting values before running - all files have been placed locally in input_directory
    input_directory = '/Users/amibening/aiken_json_files_to_combine_dir'
    output_file = 'combined_custom_dataset.json'

    # Call the function with user-provided input directory and output file
    combine_json_files(input_directory, output_file)


if __name__ == "__main__":
    main()
