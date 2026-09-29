import os
import re

directory = 'd:/article-sharing-site'
for filename in os.listdir(directory):
    if filename.endswith('.html'):
        filepath = os.path.join(directory, filename)
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 1. Update the navbar link text in all files
        # <a href="books.html">几页书</a> -> <a href="books.html">三分钟让你成为文青</a>
        content = re.sub(r'<a href="books.html"([^>]*)>几页书</a>', r'<a href="books.html"\1>三分钟让你成为文青</a>', content)
        
        # 2. Update books.html specifically
        if filename == 'books.html':
            content = content.replace('<title>Empathy - 几页书</title>', '<title>三分钟让你成为文青 - Empathy</title>')
            content = content.replace('<h1>几页书</h1>', '<h1>三分钟让你成为文青</h1>')
            # Remove the subtitle
            content = re.sub(r'<p>”pathy”意思是「感覺」.*?就像在對方心裡頭的感受</p>', '', content, flags=re.DOTALL)
            
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
