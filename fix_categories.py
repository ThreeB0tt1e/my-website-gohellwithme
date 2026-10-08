import os
import re

directory = 'd:/article-sharing-site'

# The actual list of articles from old git history
articles_data = {
    '今日杂谈': [
        ('miscellany5.html', '不再自取其辱', '2026-09-24'),
        ('miscellany4.html', '被同事孤立', '2026-09-24'),
        ('miscellany3.html', '内耗', '2026-09-24'),
        ('miscellany2.html', '不低头病', '2026-09-24'),
        ('miscellany1.html', '一段好坏交替的日子', '2026-09-24')
    ],
    '游记': [
        ('travel-extra.html', '游记番外', '2026-09-24'),
        ('travel2.html', '游记 2', '2026-09-24')
    ],
    '寓言': [
        ('untitled.html', '无题', '2026-09-24')
    ],
    '糖果屋': [
        ('tangguowu.html', '糖果屋', '2026-09-24')
    ]
}

template = '''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} - Empathy</title>
    <link rel="stylesheet" href="styles.css?v=202610081840">
    <link href="https://fonts.googleapis.com/css2?family=Playfair+Display:ital@1&display=swap" rel="stylesheet">
    <style>
        .chapter-list { max-width: 600px; margin: 0 auto 60px; display: flex; flex-direction: column; gap: 15px; }
        .chapter-item { display: flex; justify-content: space-between; align-items: center; padding: 20px; background: var(--card-bg); border: 1px solid var(--border-color); border-radius: 4px; text-decoration: none; color: var(--text-color); transition: transform 0.2s, box-shadow 0.2s; }
        .chapter-item:hover { transform: translateX(5px); box-shadow: 0 4px 12px rgba(0,0,0,0.05); }
        .chapter-num { font-family: 'Playfair Display', serif; color: var(--text-muted); font-size: 0.9rem; }
        .chapter-title { font-weight: 500; }
    </style>
</head>
<body>
    <nav class="navbar">
        <div class="container nav-container">
            <div class="nav-logo">Empathy</div>
            <button class="nav-toggle" aria-label="Toggle Navigation">
                <span></span>
                <span></span>
                <span></span>
            </button>
            <div class="nav-links">
                <a href="index.html">首页</a>
                <a href="articles.html" class="active">目录</a>
                <a href="contract.html">魔鬼契约</a>
                <a href="books.html">三分钟让你成为文青</a>
                <a href="characters.html">人物介绍</a>
                <a href="guestbook.html">留言板</a>
            </div>
        </div>
    </nav>

    <main class="container">
        <nav class="breadcrumb" style="margin-top: 20px;">
            <a href="articles.html">全部分类</a> / <a href="#">← 返回 {title}</a>
        </nav>

        <div class="book-cover" style="text-align: center; padding: 60px 20px; border-bottom: 1px solid var(--border-color); margin-bottom: 40px;">
            <h1 style="font-size: 3rem; margin-bottom: 15px; font-family: 'Playfair Display', 'Noto Serif SC', serif;">{title}</h1>
        </div>

        <div class="chapter-list">
            {links}
        </div>
    </main>

    <script src="main.js?v=202610081840"></script>
</body>
</html>'''

filenames = {
    '今日杂谈': 'cat_today.html',
    '游记': 'cat_travel.html',
    '寓言': 'cat_fable.html',
    '糖果屋': 'cat_candy.html'
}

for cat, items in articles_data.items():
    links_html = ''
    for link, name, date in items:
        links_html += f'''
            <a href="{link}" class="chapter-item">
                <span class="chapter-title">{name}</span>
                <span style="color: var(--text-muted);">→</span>
            </a>'''
            
    page_html = template.replace('{title}', cat).replace('{links}', links_html)
    with open(os.path.join(directory, filenames[cat]), 'w', encoding='utf-8') as f:
        f.write(page_html)

# Update articles.html to point to these files
with open(os.path.join(directory, 'articles.html'), 'r', encoding='utf-8') as f:
    content = f.read()

# Replace the archive-list with the full correct one
new_archive_list = '''<div class="archive-list">
            <a href="contract.html" class="archive-item">
                <div class="archive-title">
                    <span>魔鬼契约</span>
                    <span class="archive-meta">Series 01</span>
                </div>
            </a>
            <a href="cat_today.html" class="archive-item">
                <div class="archive-title">
                    <span>今日杂谈</span>
                    <span class="archive-meta">Series 02</span>
                </div>
            </a>
            <a href="cat_travel.html" class="archive-item">
                <div class="archive-title">
                    <span>游记</span>
                    <span class="archive-meta">Series 03</span>
                </div>
            </a>
            <a href="cat_fable.html" class="archive-item">
                <div class="archive-title">
                    <span>寓言</span>
                    <span class="archive-meta">Series 04</span>
                </div>
            </a>
            <a href="cat_candy.html" class="archive-item">
                <div class="archive-title">
                    <span>糖果屋</span>
                    <span class="archive-meta">Series 05</span>
                </div>
            </a>
            <a href="books.html" class="archive-item">
                <div class="archive-title">
                    <span>三分钟让你成为文青</span>
                    <span class="archive-meta">Series 06</span>
                </div>
            </a>
            <a href="characters.html" class="archive-item">
                <div class="archive-title">
                    <span>人物介绍</span>
                    <span class="archive-meta">Series 07</span>
                </div>
            </a>
        </div>'''

content = re.sub(r'<div class="archive-list">.*?</div>\s*<!-- We keep the category containers hidden', new_archive_list + '\n        <!-- We keep the category containers hidden', content, flags=re.DOTALL)

with open(os.path.join(directory, 'articles.html'), 'w', encoding='utf-8') as f:
    f.write(content)