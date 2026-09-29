import re

with open('articles.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Extract all chapter-items
pattern = r'<a href="[^"]+" class="chapter-item card" data-category="[^"]+" style="text-decoration: none;">.*?</a>'
matches = re.findall(pattern, html, re.DOTALL)
articles_html = '\n'.join(matches)

# Rebuild entire articles.html
new_html = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Chapter - Empathy</title>
    <meta name="robots" content="noindex, nofollow">
    <link rel="stylesheet" href="styles.css">
    <link href="https://fonts.googleapis.com/css2?family=Playfair+Display:ital@1&display=swap" rel="stylesheet">
</head>
<body>
    <nav class="navbar">
        <div class="container nav-container">
            <div class="nav-logo">Empathy</div>
            <button class="nav-toggle" aria-label="Toggle Navigation">
                <span></span><span></span><span></span>
            </button>
            <div class="nav-links">
                <a href="index.html">首页</a>
                <a href="articles.html" class="active">目录</a>
                <a href="contract.html">魔鬼契约</a>
                <a href="books.html">几页书</a>
                <a href="characters.html">人物介绍</a>
                <a href="guestbook.html">留言板</a>
            </div>
        </div>
    </nav>
    <header>
        <div class="container">
            <h1 style="font-family: 'Playfair Display', 'Noto Serif SC', serif;">Chapter</h1>
            <p class="gong-er-quote js-enabled">“习武之人有三个阶段：见自己，见天地，见众生。” <span class="author">—— 宫二</span></p>
        </div>
    </header>

    <main class="container">
        
        <div class="folding-screen-container js-enabled">
            <!-- 第一扇：见自己 -->
            <div class="screen-panel">
                <h2 class="panel-title">见自己</h2>
                <div class="panel-options">
                    <button class="filter-btn" onclick="filterCategory('今日杂谈', this)">今日杂谈</button>
                    <button class="filter-btn" onclick="filterCategory('游记', this)">游记</button>
                </div>
            </div>
            
            <!-- 第二扇：见天地 -->
            <div class="screen-panel">
                <h2 class="panel-title">见天地</h2>
                <div class="panel-options">
                    <button class="filter-btn" onclick="filterCategory('寓言', this)">寓言</button>
                    <button class="filter-btn" onclick="filterCategory('糖果屋', this)">糖果屋</button>
                </div>
            </div>
            
            <!-- 第三扇：见众生 -->
            <div class="screen-panel">
                <h2 class="panel-title">见众生</h2>
                <div class="panel-options">
                    <button class="filter-btn" onclick="filterCategory('魔鬼契约', this)">魔鬼契约</button>
                    <button class="filter-btn" onclick="filterCategory('all', this)">[ 展开全部 ]</button>
                </div>
            </div>
        </div>

        <div class="article-grid js-enabled" style="display: none; flex-direction: column; gap: 15px;">
{articles_html}
        </div>
    </main>

    <footer>
        <div class="container">
            <p>© 2026 Empathy. 保留所有权利，包括保持沉默的权利。</p>
        </div>
    </footer>

    <script>
        function filterCategory(cat, btn) {{
            document.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active'));
            if(btn) btn.classList.add('active');
            
            const grid = document.querySelector('.article-grid');
            grid.style.display = 'flex';
            
            // 简单的淡入动画逻辑
            grid.style.opacity = '0';
            setTimeout(() => {{
                document.querySelectorAll('.chapter-item').forEach(article => {{
                    if (cat === 'all' || article.getAttribute('data-category') === cat) {{
                        article.style.display = 'flex';
                    }} else {{
                        article.style.display = 'none';
                    }}
                }});
                grid.style.opacity = '1';
                grid.style.transition = 'opacity 0.8s ease';
            }}, 50);
            
            // 滚动到列表位置
            setTimeout(() => {{
                grid.scrollIntoView({{ behavior: 'smooth', block: 'start' }});
            }}, 200);
        }}
    </script>
    <script src="https://cdn.jsdelivr.net/npm/medium-zoom@1.1.0/dist/medium-zoom.min.js" async></script>
    <script src="main.js"></script>
</body>
</html>
'''

with open('articles.html', 'w', encoding='utf-8') as f:
    f.write(new_html)

