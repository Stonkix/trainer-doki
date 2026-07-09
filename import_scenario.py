import json
import os
import traceback
import sys

# Default Configuration
DEFAULT_JSON_FILE = r"C:\Users\alexa\Desktop\astraldocs\Авторизация водителя в мобильной версии Доки.json"
DEFAULT_PREFIX = "mobile_1"
OUTPUT_DIR = r"C:\Users\alexa\Desktop\Работа\astraldocs\astraldocs"
IMAGE_DIR = r"C:\Users\alexa\Desktop\Работа\astraldocs\astraldocs\images"

# Template based on etrn_t1_1.html
TEMPLATE = """<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <link rel="stylesheet" href="./styles/scenariopagestyle.css">
    <style>
        .tooltip-show {{ background-color: #7c5cfc !important; }}
        .hotspot {{ 
            position: absolute; 
            cursor: pointer; 
            border: 2px solid rgba(124, 92, 252, 0.5); 
            background: rgba(124, 92, 252, 0.2); 
            display: none; 
            z-index: 100;
            animation: pulse 2s infinite ease-in-out;
            transform-origin: center;
            border-radius: 4px;
            pointer-events: auto !important;
        }}
        .hotspot:hover {{ background: rgba(124, 92, 252, 0.4); }}
        @keyframes pulse {{
            0% {{ transform: scale(1); opacity: 0.6; }}
            50% {{ transform: scale(1.05); opacity: 0.9; }}
            100% {{ transform: scale(1); opacity: 0.6; }}
        }}
    </style>
</head>
<body>
    <header class="header">
        <div class="nav-buttons">
            <button class="nav-button" onclick="window.location.href='./index.html'">
                <img src="./assets/icons/arrowLeft.svg" alt="Назад">
            </button>
            <button class="nav-button" onclick="window.location.href='./index.html'">
                <img src="./assets/icons/exitButton.svg" alt="На главную">
            </button>
            <button class="nav-button" onclick="window.location.href='{next_page}'">
                <img src="./assets/icons/arrowRight.svg" alt="Вперёд">
            </button>
        </div>
        <div class="logo-and-title">
            <div class="logo">
                <img src="./Icon_Astal_Docs_color_v1.png" alt="Логотип">
            </div>
            <div class="header-title">Доки</div>
        </div>
        <div class="nav-buttons"></div>
    </header>
    <div class="background-container">
        <div class="image-wrapper">
            <img src="{img_src}" id="step-img" alt="Экран">
            <div class="hotspot-container" id="hotspot-container">
                <div class="tooltip tooltip-show" id="main-tooltip" style="left: 50%; top: 40%; transform: translate(-50%, -50%) scale(1); opacity: 1; z-index: 20;">
                    <div class="tooltip-title" id="tooltip-title"></div>
                    <div class="tooltip-inner" id="tooltip-inner"></div>
                    <div class="tooltip-actions">
                        <button class="next" id="dialogue-next-button" onclick="handleNext()">Далее</button>
                    </div>
                    <img src="./assets/icons/mascotRight.svg" class="tooltip-mascot tooltip-mascot-left mascot-show" alt="Маскот">
                </div>
            </div>
        </div>
    </div>
    <script>
        const steps = {steps_json};
        const clickZones = {click_zones_json};
        let currentStep = 0;
        function handleNext() {{
            const titleEl = document.getElementById('tooltip-title');
            const contentEl = document.getElementById('tooltip-inner');
            const tooltip = document.getElementById('main-tooltip');
            const btn = document.getElementById('dialogue-next-button');
            
            if (currentStep < steps.length - 1) {{
                currentStep++;
                contentEl.style.opacity = 0;
                titleEl.style.opacity = 0;
                setTimeout(() => {{
                    titleEl.textContent = steps[currentStep].title;
                    contentEl.innerHTML = steps[currentStep].content;
                    titleEl.style.visibility = steps[currentStep].title ? 'visible' : 'hidden';
                    tooltip.style.left = steps[currentStep].x + '%';
                    tooltip.style.top = steps[currentStep].y + '%';
                    contentEl.style.opacity = 1;
                    titleEl.style.opacity = 1;
                    if (currentStep === steps.length - 1 && '{is_last_page}' === 'true') {{
                        btn.textContent = 'Завершить';
                    }} else {{
                        btn.textContent = 'Далее';
                    }}
                }}, 250);
            }} else {{
                if ('{is_last_page}' === 'true') {{
                    window.location.href = '{end_page}';
                }} else {{
                    tooltip.style.display = 'none';
                    document.querySelectorAll('.hotspot').forEach(h => h.style.display = 'block');
                }}
            }}
        }}
        document.addEventListener('DOMContentLoaded', () => {{
            const titleEl = document.getElementById('tooltip-title');
            const contentEl = document.getElementById('tooltip-inner');
            const tooltip = document.getElementById('main-tooltip');
            const btn = document.getElementById('dialogue-next-button');
            titleEl.textContent = steps[0].title;
            contentEl.innerHTML = steps[0].content;
            titleEl.style.visibility = steps[0].title ? 'visible' : 'hidden';
            tooltip.style.left = steps[0].x + '%';
            tooltip.style.top = steps[0].y + '%';

            if (steps.length === 1 && '{is_last_page}' === 'true') {{
                btn.textContent = 'Завершить';
            }} else {{
                btn.textContent = 'Далее';
            }}

            const container = document.getElementById('hotspot-container');
            clickZones.forEach(z => {{
                const div = document.createElement('div');
                div.className = 'hotspot';
                div.style.left = z.x + '%';
                div.style.top = z.y + '%';
                div.style.width = z.w + '%';
                div.style.height = z.h + '%';
                div.onclick = () => window.location.href = z.action;
                container.appendChild(div);
            }});
        }});
    </script>
</body>
</html>
"""

def main():
    json_file = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_JSON_FILE
    prefix = sys.argv[2] if len(sys.argv) > 2 else DEFAULT_PREFIX

    if not os.path.exists(json_file):
        print(f"Error: {json_file} not found.")
        return

    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

    for i, step_data in enumerate(data):
        # Filename: mobile_1_1.html, mobile_1_2.html, etc.
        filename = f"{prefix}_{i+1}.html"
        filepath = os.path.join(OUTPUT_DIR, filename)
        
        title = step_data.get('label', f"Шаг {i+1}")
        img_name = f"{prefix}_{i+1}.png"
        img_src = f"./images/{img_name}"
        
        # Determine next page for the header button
        next_page = "index.html"
        if i < len(data) - 1:
            next_page = f"{prefix}_{i+2}.html"
        else:
            next_page = "index.html"

        # Prepare steps (tooltips)
        steps_for_html = []
        for t in step_data.get('steps', []):
            steps_for_html.append({
                "title": t.get('title', ''),
                "content": t.get('content', ''),
                "x": t.get('x', 50),
                "y": t.get('y', 50)
            })
        
        # Prepare click zones
        click_zones_for_html = []
        for cz in step_data.get('clickZones', []):
            click_zones_for_html.append({
                "x": cz.get('x', 0),
                "y": cz.get('y', 0),
                "w": cz.get('w', 0),
                "h": cz.get('h', 0),
                "action": cz.get('action', '')
            })

        html_content = TEMPLATE.format(
            title=title,
            next_page=next_page,
            img_src=img_src,
            steps_json=json.dumps(steps_for_html, ensure_ascii=False),
            click_zones_json=json.dumps(click_zones_for_html, ensure_ascii=False),
            is_last_page="true" if i == len(data) - 1 else "false",
            end_page="end.html"
        )

        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(html_content)
        print(f"Created {filepath}")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"An error occurred: {e}")
        traceback.print_exc()
