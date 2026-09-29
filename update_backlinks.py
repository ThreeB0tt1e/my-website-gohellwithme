import os
import re

directory = 'd:/article-sharing-site'

# 1. Parse articles.html to get category mapping
with open(os.path.join(directory, 'articles.html'), 'r', encoding='utf-8') as f:
    dir_html = f.read()

# Pattern: <a href="filename.html" class="chapter-item" data-category="category"
cat_map = {}
matches = re.finditer(r'<a href="([^"]+\.html)"[^>]*data-category="([^"]+)"', dir_html)
for m in matches:
    cat_map[m.group(1)] = m.group(2)

# 2. Iterate and replace
for filename in os.listdir(directory):
    if filename.endswith('.html') and filename not in ['index.html', 'articles.html', 'admin.html', 'admin-article.html', 'books.html', 'characters.html', 'contract.html', 'guestbook.html', 'article-template.html']:
        
        filepath = os.path.join(directory, filename)
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Only process if it has a category
        if filename in cat_map:
            cat = cat_map[filename]
            
            breadcrumb = f'''<div class="article-breadcrumb" style="margin-bottom: 25px; font-size: 0.95rem; font-family: 'Noto Serif SC', serif;">
    <a href="articles.html" style="color: var(--text-muted); text-decoration: none;">屏风大厅</a> 
    <span style="color: var(--border-color); margin: 0 10px;">/</span> 
    <a href="articles.html#categories" style="color: var(--text-muted); text-decoration: none;">全部分类</a>
    <span style="color: var(--border-color); margin: 0 10px;">/</span> 
    <a href="articles.html#cat-{cat}" style="color: var(--text-color); text-decoration: none;">← 返回 {cat}</a>
</div>'''

            # Replace old back links. We have two formats:
            # <a href="articles.html" class="back-link">← 返回目录</a>
            content = re.sub(r'<a href="articles\.html" class="back-link">.*?</a>', breadcrumb, content)
            
            # <a href="articles.html" class="nav-prev">← 返回目录</a>
            content = re.sub(r'<a href="articles\.html" class="nav-prev">← 返回目录</a>', breadcrumb, content)
            
            # Some might just be <a href="articles.html">← 返回目录</a>
            content = re.sub(r'<a href="articles\.html"[^>]*>← 返回目录</a>', breadcrumb, content)

            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)

# We also need to update admin-article.html so future articles get the breadcrumb!
# Wait, admin-article.html creates the HTML template as a string. We can update it too.
admin_path = os.path.join(directory, 'admin-article.html')
if os.path.exists(admin_path):
    with open(admin_path, 'r', encoding='utf-8') as f:
        admin = f.read()
    
    old_back = r'<a href="articles\.html" class="nav-prev">← 返回目录</a>'
    new_back = r'''<div class="article-breadcrumb" style="margin-bottom: 25px; font-size: 0.95rem; font-family: \'Noto Serif SC\', serif;">
                    <a href="articles.html" style="color: var(--text-muted); text-decoration: none;">屏风大厅</a> 
                    <span style="color: var(--border-color); margin: 0 10px;">/</span> 
                    <a href="articles.html#categories" style="color: var(--text-muted); text-decoration: none;">全部分类</a>
                    <span style="color: var(--border-color); margin: 0 10px;">/</span> 
                    <a href="articles.html#cat-" style="color: var(--text-color); text-decoration: none;">← 返回 </a>
                </div>'''
    
    admin = re.sub(old_back, new_back, admin)
    with open(admin_path, 'w', encoding='utf-8') as f:
        f.write(admin)

