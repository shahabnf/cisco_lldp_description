import os
import shutil
import glob

def create_or_empty_output_folder(folder_path):
    """Creates the output folder if it does not exist or empties it if it does."""
    if os.path.exists(folder_path):
        # Empty the folder
        for file in os.listdir(folder_path):
            file_path = os.path.join(folder_path, file)
            if os.path.isfile(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        print(f"Emptied folder: {folder_path}")
    else:
        os.makedirs(folder_path)
        print(f"Created folder: {folder_path}")

def move_files_to_output_folder(source_path, destination_folder):
    """Moves all files starting with 'output' to the output folder."""
    files = glob.glob(os.path.join(source_path, "output*"))
    
    if not files:
        print("No files starting with 'output' found.")
        return
    
    for file in files:
        shutil.move(file, destination_folder)
        # print(f"Moved {file} to {destination_folder}")
    print("All files starting with 'output' moved to the output folder.")

def main():
    # Define the path for the new output directory
    output_folder_path = os.path.join(os.getcwd(), "output")
    
    # Create or empty the output directory
    create_or_empty_output_folder(output_folder_path)
    
    # Move files starting with 'output' to the new output folder
    move_files_to_output_folder(os.getcwd(), output_folder_path)

if __name__ == "__main__":
    main()
