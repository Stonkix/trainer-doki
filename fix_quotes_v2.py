import json
import re
import glob

def fix_text_quotes(text):
    if not text:
        return text
    # Replace curly quotes
    text = text.replace('“', '«').replace('”', '»')
    # Replace standard double quotes that are likely used as quotes in text (not HTML attributes)
    # This is tricky. We look for " a word " patterns.
    # A better way is to replace all " with « or » if they are not part of JSON structure.
    # But we are already inside a string value from json.load(), so the " we see are literal quotes.
    
    # We want to replace "..." with «...»
    # We can use a regex to find quotes that surround text.
    # For simplicity, if we are in a <p> tag, we can try to replace standard quotes.
    
    # Replace standard double quotes with guillemets if they seem to be pairs.
    # Since we are processing the string content, any " here is a literal double quote.
    # We replace the first " with « and the second with » in pairs.
    
    count = 0
    new_text = []
    for char in text:
        if char == '"':
            count += 1
            new_text.append('«' if count % 2 != 0 else '»')
        else:
            new_text.append(char)
    
    # If there's an odd number of quotes, the last one should probably be " or something else.
    # But usually they come in pairs.
    
    return "".join(new_text)

def process_json_files():
    # Target specific file or all
    json_files = glob.glob(r"C:\Users\alexa\Desktop\Работа\astraldocs\*.json")
    for file_path in json_files:
        with open(file_path, "r", encoding="utf-8") as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                continue

        def walk_and_fix(obj):
            if isinstance(obj, dict):
                # Only fix 'content' fields to avoid breaking IDs or labels
                new_dict = {}
                for k, v in obj.items():
                    if k == 'content' and isinstance(v, str):
                        new_dict[k] = fix_text_quotes(v)
                    else:
                        new_dict[k] = walk_and_fix(v)
                return new_dict
            elif isinstance(obj, list):
                return [walk_and_fix(i) for i in obj]
            else:
                return obj

        fixed_data = walk_and_fix(data)
        
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(fixed_data, f, ensure_ascii=False, indent=4)
        print(f"Fixed quotes in {file_path}")

if __name__ == "__main__":
    process_json_files()
