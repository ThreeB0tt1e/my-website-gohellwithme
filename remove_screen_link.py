import os
import re

directory = 'd:/article-sharing-site'

for filename in os.listdir(directory):
    if filename.endswith('.html') and filename not in ['index.html', 'articles.html', 'admin.html', 'books.html', 'characters.html', 'contract.html', 'guestbook.html', 'article-template.html']:
        filepath = os.path.join(directory, filename)
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Remove the 屏风大厅 part from the breadcrumb
        old_breadcrumb_part = r'<a href="articles\.html" style="color: var\(--text-muted\); text-decoration: none;">屏风大厅</a>\s*<span style="color: var\(--border-color\); margin: 0 10px;">/</span>'
        
        content = re.sub(old_breadcrumb_part, '', content)

        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)

# Also update admin-article.html
admin_path = os.path.join(directory, 'admin-article.html')
if os.path.exists(admin_path):
    with open(admin_path, 'r', encoding='utf-8') as f:
        admin = f.read()
    
    old_breadcrumb_part = r'<a href="articles\.html" style="color: var\(--text-muted\); text-decoration: none;">屏风大厅</a>\s*<span style="color: var\(--border-color\); margin: 0 10px;">/</span>'
    admin = re.sub(old_breadcrumb_part, '', admin)
    with open(admin_path, 'w', encoding='utf-8') as f:
        f.write(admin)

