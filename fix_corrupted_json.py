import re

def fix_corrupted_json(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Find all patterns of "content": "..."
    # We use a non-greedy match for the content.
    # We assume the content starts with <p> and ends with </p>
    
    def replace_quotes(match):
        prefix = match.group(1)
        text = match.group(2)
        suffix = match.group(3)
        
        # In the text, replace " with « or »
        count = 0
        new_text = []
        for char in text:
            if char == '"':
                count += 1
                new_text.append('«' if count % 2 != 0 else '»')
            else:
                new_text.append(char)
        
        return f'{prefix}{"".join(new_text)}{suffix}'

    # Regex to find "content": "..."
    # It looks for "content": " then anything until " followed by , or }
    pattern = r'("content":\s*")(.*?)(",\s*|\"\s*,\s*|\"$\s*|\"\s*})'
    # This regex is a bit naive. Let's try to be more specific about the <p> tags.
    pattern = r'("content":\s*")(.*?</p>)(")'
    
    fixed_content = re.sub(pattern, replace_quotes, content)
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(fixed_content)

if __name__ == "__main__":
    files_to_fix = [
        r"C:\Users\alexa\Desktop\Работа\astraldocs\Загрузка и подписание ЭТрН Т1 грузоотправителем в веб-кабинете Доки.json",
        r"C:\Users\alexa\Desktop\Работа\astraldocs\Подписание ЭТрН Т2 грузоперевозчиком в веб-кабинете Доки.json",
        r"C:\Users\alexa\Desktop\Работа\astraldocs\Подписание ЭТрН Т3 грузополучателем в веб-кабинете Доки.json",
        r"C:\Users\alexa\Desktop\Работа\astraldocs\Подписание ЭТрН Т4 грузоперевозчиком в веб-кабинете Доки.json",
        r"C:\Users\alexa\Desktop\Работа\astraldocs\Авторизация водителя в мобильной версии Доки.json",
        r"C:\Users\alexa\Desktop\Работа\astraldocs\Подписание ЭТрН Т2 водителем в мобильной версии Доки.json"
    ]
    for file_path in files_to_fix:
        fix_corrupted_json(file_path)

