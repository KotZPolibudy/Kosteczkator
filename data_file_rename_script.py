import os


def rename_files_in_folder(folder_path, subfolder_index):
    # Get a list of all files in the folder
    files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]

    # Sort files to ensure consistent renaming order
    files.sort()

    # Loop through the files and rename them
    for index, file in enumerate(files, start=1):
        # Get the file extension
        file_extension = os.path.splitext(file)[1]

        # Construct the new file name
        new_name = f"{subfolder_index}_{index}{file_extension}"

        # Rename the file
        os.rename(os.path.join(folder_path, file), os.path.join(folder_path, new_name))


def rename_files_in_data_folder(data_folder):
    # Traverse through the directory structure
    for root, dirs, files in os.walk(data_folder):
        # Skip if there are no files in the directory
        if files:
            # Determine the subfolder index based on the immediate parent directory
            subfolder_name = os.path.basename(root)
            try:
                subfolder_index = int(subfolder_name)
                print(f"Renaming files in: {root} (Subfolder index: {subfolder_index})")
                rename_files_in_folder(root, subfolder_index)
            except ValueError:
                # If the parent directory name is not a number, skip it
                continue


if __name__ == "__main__":
    # Define the path to the 'data' folder
    data_folder = os.path.join(os.getcwd(), 'data')

    # Rename files in the 'data' folder and its subdirectories
    rename_files_in_data_folder(data_folder)
