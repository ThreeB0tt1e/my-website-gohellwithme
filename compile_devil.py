import re

with open('d:/article-sharing-site/devil-contract-full.md', 'r', encoding='utf-8') as f:
    text = f.read()

text = re.sub(r'^##\s+(.*)$', r'<h2 id="\1">\1</h2>', text, flags=re.MULTILINE)

parts = text.split('\n\n')
html_parts = []
for p in parts:
    p = p.strip()
    if not p:
        continue
    if p.startswith('<h2'):
        html_parts.append(p)
    else:
        p = p.replace('\n', '<br>')
        html_parts.append(f'<p>{p}</p>')

html_content = '\n'.join(html_parts)

new_html = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>魔鬼契约 - Empathy</title>
    <link rel="stylesheet" href="styles.css?v=1790708827">
    <link href="https://fonts.googleapis.com/css2?family=Playfair+Display:ital@1&display=swap" rel="stylesheet">
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

    <header class="article-header" style="text-align: center; padding: 60px 20px; border-bottom: 1px solid var(--border-color); margin-bottom: 40px;">
        <div class="container">
            <h1 style="font-family: 'Playfair Display', 'Noto Serif SC', serif; font-size: 3rem; margin-bottom: 15px;">魔鬼契约</h1>
            <p style="color: var(--text-muted); font-size: 1rem; font-style: italic;">全文连载版</p>
        </div>
    </header>
    <main class="container">
        <nav class="breadcrumb" style="margin-bottom: 30px;">
            <a href="articles.html#categories">全部分类</a> / <a href="articles.html#cat-contract">← 返回 连载系列</a>
        </nav>
        <article class="article-content">
            {html_content}
        </article>
    </main>

    <script src="main.js?v=1790708827"></script>
</body>
</html>'''

with open('d:/article-sharing-site/contract.html', 'w', encoding='utf-8') as f:
    f.write(new_html)