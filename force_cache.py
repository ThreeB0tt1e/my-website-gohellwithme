import os
import re
import time

directory = 'd:/article-sharing-site'
timestamp = int(time.time())

for filename in os.listdir(directory):
    if filename.endswith('.html'):
        filepath = os.path.join(directory, filename)
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        content = re.sub(r'href="styles\.css(\?v=\d+)?"', f'href="styles.css?v={timestamp}"', content)
        content = re.sub(r'src="main\.js(\?v=\d+)?"', f'src="main.js?v={timestamp}"', content)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
