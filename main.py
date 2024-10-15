import io
import re
import sys
import zipfile


# Function recursively goes through each file and zip
def search_nested_zip(search_str, zip_path, parent_path=""):
    for file_name in zip_path.namelist():
        file_path = f"{parent_path}/{file_name}" if parent_path else file_name
        try:
            with zip_path.open(file_name) as file:
                if file_name.endswith('.zip'):
                    with zipfile.ZipFile(io.BytesIO(file.read())) as nested_zip:
                        search_nested_zip(search_str, nested_zip, file_path)
                else:
                    for line in file:
                        line = line.decode('utf-8', errors='ignore')
                        if re.search(search_str, line):
                            print(line.strip())
                            
        except Exception as e:
            print(f"Could not read {file_path}: {e}")
                            
                        
# Opens the original zip file
def search_zip_file(search_str, zip_path):
    try:
        with zipfile.ZipFile(zip_path, "r") as zip_ref:
            search_nested_zip(search_str, zip_ref)
    except Exception as e:
        print(f"Could not open {zip_path}: {e}")

# Main 
if __name__ == "__main__":
    # Check if two additional arguments are given
    if len(sys.argv) != 3:
        search_str = input("String: ")
        zip_path = input("Directory: ")
    else:
        search_str = sys.argv[1]
        zip_path = sys.argv[2]

    # Call the Search Zip Files Function
    search_zip_file(search_str, zip_path)
    