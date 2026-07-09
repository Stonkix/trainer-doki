import json
import re
import glob

def restore_json_structure(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
    
    # Replace corrupted quotes back to double quotes
    fixed = content.replace("»", '"').replace("«", '"')
    
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(fixed)

# List of files to restore
files = glob.glob(r"C:\Users\alexa\Desktop\Работа\astraldocs\*.json")
for f in files:
    restore_json_structure(f)
