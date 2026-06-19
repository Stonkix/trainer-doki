import os
import re

directory = r"C:\Users\alexa\Desktop\astraldocs\astraldocs"

replacements = [
    (r"\.\./styles/", "./styles/"),
    (r"\.\./assets/", "./assets/"),
    (r"\.\./Icon_Astal_Docs_color_v1.png", "./Icon_Astal_Docs_color_v1.png"),
    (r"\.\./images/", "./images/"),
    (r"\.\./index.html", "./index.html"),
]

def fix_paths():
    if not os.path.exists(directory):
        print(f"Error: {directory} does not exist.")
        return

    for filename in os.listdir(directory):
        if filename.startswith("mobile_1_") and filename.endswith(".html"):
            filepath = os.path.join(directory, filename)
            print(f"Processing {filepath}")
            
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            new_content = content
            for old, new in replacements:
                new_content = re.sub(old, new, new_content)
            
            if new_content != content:
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                print(f"Updated {filename}")
            else:
                print(f"No changes needed for {filename}")

if __name__ == "__main__":
    fix_paths()
