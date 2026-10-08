contract_content = '''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>魔鬼契约 - Empathy</title>
    <link rel="stylesheet" href="styles.css?v=202610081627">
    <link href="https://fonts.googleapis.com/css2?family=Playfair+Display:ital@1&display=swap" rel="stylesheet">
    <style>
        .book-cover {
            text-align: center;
            padding: 60px 20px;
            border-bottom: 1px solid var(--border-color);
            margin-bottom: 40px;
        }
        .book-cover h1 {
            font-size: 3rem;
            margin-bottom: 15px;
            font-family: 'Playfair Display', "Noto Serif SC", serif;
        }
        .book-cover p {
            color: var(--text-muted);
            font-size: 1.1rem;
            max-width: 600px;
            margin: 0 auto;
            font-style: italic;
        }
        .chapter-list {
            max-width: 600px;
            margin: 0 auto 60px;
            display: flex;
            flex-direction: column;
            gap: 15px;
        }
        .chapter-item {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 20px;
            background: var(--card-bg);
            border: 1px solid var(--border-color);
            border-radius: 4px;
            text-decoration: none;
            color: var(--text-color);
            transition: transform 0.2s, box-shadow 0.2s;
        }
        .chapter-item:hover {
            transform: translateX(5px);
            box-shadow: 0 4px 12px rgba(0,0,0,0.05);
        }
        .chapter-num {
            font-family: 'Playfair Display', serif;
            color: var(--text-muted);
            font-size: 0.9rem;
        }
        .chapter-title {
            font-weight: 500;
        }
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
                <a href="articles.html">目录</a>
                <a href="contract.html" class="active">魔鬼契约</a>
                <a href="books.html">三分钟让你成为文青</a>
                <a href="characters.html">人物介绍</a>
                <a href="guestbook.html">留言板</a>
            </div>
        </div>
    </nav>

    <main class="container">
        <nav class="breadcrumb" style="margin-top: 20px;">
            <a href="articles.html#categories">全部分类</a> / <a href="articles.html#cat-contract">← 返回 连载系列</a>
        </nav>

        <div class="book-cover">
            <h1>魔鬼契约</h1>
            <p>Empathy，意思是“共情”。但在魔鬼的契约里，共情往往是深渊的开始。</p>
        </div>

        <div class="chapter-list">
            <a href="devil_1.html" class="chapter-item">
                <span class="chapter-title">魔鬼契约 序</span>
                <span style="color: var(--text-muted);">→</span>
            </a>
            <a href="devil_2.html" class="chapter-item">
                <span class="chapter-title">魔鬼契约 1</span>
                <span style="color: var(--text-muted);">→</span>
            </a>
            <a href="devil_3.html" class="chapter-item">
                <span class="chapter-title">魔鬼契约 2</span>
                <span style="color: var(--text-muted);">→</span>
            </a>
            <a href="devil_4.html" class="chapter-item">
                <span class="chapter-title">魔鬼契约 3——清道夫</span>
                <span style="color: var(--text-muted);">→</span>
            </a>
            <a href="devil_5.html" class="chapter-item">
                <span class="chapter-title">魔鬼契约——番外</span>
                <span style="color: var(--text-muted);">→</span>
            </a>
            <a href="devil_6.html" class="chapter-item">
                <span class="chapter-title">魔鬼契约 4</span>
                <span style="color: var(--text-muted);">→</span>
            </a>
            <a href="devil_7.html" class="chapter-item">
                <span class="chapter-title">魔鬼契约 5 忍者 上</span>
                <span style="color: var(--text-muted);">→</span>
            </a>
            <a href="devil_8.html" class="chapter-item">
                <span class="chapter-title">魔鬼契约 5 忍者 中</span>
                <span style="color: var(--text-muted);">→</span>
            </a>
            <a href="devil_9.html" class="chapter-item">
                <span class="chapter-title">魔鬼契外（6）贱人命长</span>
                <span style="color: var(--text-muted);">→</span>
            </a>
        </div>
    </main>

    <script src="main.js?v=202610081627"></script>
</body>
</html>
'''

with open('d:/article-sharing-site/contract.html', 'w', encoding='utf-8') as f:
    f.write(contract_content)