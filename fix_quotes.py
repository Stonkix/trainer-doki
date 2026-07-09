import os
import json
import re
import glob

def fix_quotes(text):
    # Pattern to find text between any of the quote characters
    # It looks for a starting quote, then any characters that are NOT quotes, then an ending quote.
    pattern = r"([“”«»])([^“”«»]+)([“”«»])"
    
    def replace_match(match):
        return f"«{match.group(2)}»"
    
    while True:
        new_text = re.sub(pattern, replace_match, text)
        if new_text == text:
            break
        text = new_text
    return text

def process_json_files():
    json_files = glob.glob(r"C:\Users\alexa\Desktop\Работа\astraldocs\*.json")
    for file_path in json_files:
        with open(file_path, "r", encoding="utf-8") as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                print(f"Error decoding {file_path}")
                continue

        # We need to recursively walk the JSON and fix strings
        def walk_and_fix(obj):
            if isinstance(obj, dict):
                return {k: walk_and_fix(v) for k, v in obj.items()}
            elif isinstance(obj, list):
                return [walk_and_fix(i) for i in obj]
            elif isinstance(obj, str):
                return fix_quotes(obj)
            return obj

        fixed_data = walk_and_fix(data)
        
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(fixed_data, f, ensure_ascii=False, indent=4)
        print(f"Fixed quotes in {file_path}")

if __name__ == "__main__":
    process_json_files()
