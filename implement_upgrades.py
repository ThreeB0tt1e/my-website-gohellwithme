import os
import re

# 1. Update styles.css
css_addition = '''
/* =========================================
   文章自动目录 (TOC)
   ========================================= */
.article-toc {
    position: fixed;
    top: 150px;
    left: max(20px, calc(50% - 620px));
    width: 220px;
    max-height: calc(100vh - 200px);
    overflow-y: auto;
    background: transparent;
    font-family: "Noto Serif SC", serif;
    opacity: 0;
    transition: opacity 0.5s;
    scrollbar-width: none;
}
.article-toc::-webkit-scrollbar {
    display: none;
}
.article-toc.visible {
    opacity: 1;
}
.article-toc .toc-title {
    font-size: 0.85rem;
    color: var(--text-muted);
    margin-bottom: 15px;
    letter-spacing: 2px;
    border-bottom: 1px solid var(--border-color);
    padding-bottom: 10px;
}
.article-toc ul {
    list-style: none;
    padding: 0;
    margin: 0;
}
.article-toc li {
    margin-bottom: 12px;
}
.article-toc .toc-h3 {
    padding-left: 15px;
    font-size: 0.85rem;
}
.article-toc a {
    color: var(--text-muted);
    text-decoration: none;
    font-size: 0.9rem;
    transition: color 0.3s;
    display: block;
    line-height: 1.5;
}
.article-toc a:hover, .article-toc a.active {
    color: var(--text-color);
}
@media (max-width: 1250px) {
    .article-toc {
        position: static;
        width: 100%;
        margin-bottom: 40px;
        padding: 20px;
        background: var(--card-bg);
        border: 1px solid var(--border-color);
        border-radius: 4px;
    }
}
'''
with open('d:/article-sharing-site/styles.css', 'a', encoding='utf-8') as f:
    f.write(css_addition)


# 2. Update main.js
js_addition = '''
// === 自动生成文章目录 (TOC) ===
document.addEventListener('DOMContentLoaded', () => {
    const articleContent = document.querySelector('.article-content');
    if (!articleContent) return;

    const headers = articleContent.querySelectorAll('h2, h3');
    if (headers.length < 2) return; // 标题太少不需要目录

    const tocContainer = document.createElement('div');
    tocContainer.className = 'article-toc js-enabled';
    
    const tocTitle = document.createElement('div');
    tocTitle.className = 'toc-title';
    tocTitle.innerText = '目录';
    tocContainer.appendChild(tocTitle);

    const tocList = document.createElement('ul');
    
    headers.forEach((header, index) => {
        if (!header.id) {
            header.id = 'heading-' + index;
        }
        
        const li = document.createElement('li');
        li.className = 'toc-item toc-' + header.tagName.toLowerCase();
        
        const a = document.createElement('a');
        a.href = '#' + header.id;
        a.innerText = header.innerText;
        
        a.addEventListener('click', (e) => {
            e.preventDefault();
            header.scrollIntoView({ behavior: 'smooth' });
            history.pushState(null, null, '#' + header.id);
        });
        
        li.appendChild(a);
        tocList.appendChild(li);
    });
    
    tocContainer.appendChild(tocList);
    
    // 如果屏幕小，插入到正文前；否则放到 body 下悬浮
    if (window.innerWidth <= 1250) {
        articleContent.insertBefore(tocContainer, articleContent.firstChild);
    } else {
        document.body.appendChild(tocContainer);
    }
    
    // 监听滚动高亮
    const observer = new IntersectionObserver(entries => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                document.querySelectorAll('.article-toc a').forEach(a => a.classList.remove('active'));
                const activeLink = document.querySelector(.article-toc a[href="#"]);
                if (activeLink) activeLink.classList.add('active');
            }
        });
    }, { rootMargin: '0px 0px -80% 0px' });
    
    headers.forEach(h => observer.observe(h));
});
'''
with open('d:/article-sharing-site/main.js', 'a', encoding='utf-8') as f:
    f.write(js_addition)

# 3. Update admin-article.html for Markdown Editor
with open('d:/article-sharing-site/admin-article.html', 'r', encoding='utf-8') as f:
    admin_html = f.read()

# Add marked.js script
if 'marked.min.js' not in admin_html:
    admin_html = admin_html.replace('</head>', '<script src="https://cdn.jsdelivr.net/npm/marked/marked.min.js"></script>\n</head>')

# Replace textarea with split editor
old_textarea = r'<textarea id="content" placeholder="文章正文" required></textarea>'
new_editor = '''<div style="display: flex; gap: 20px; margin-bottom: 20px;">
                <textarea id="content" placeholder="在此使用 Markdown 语法写作... (支持用 # 表示标题，便于生成目录)" required style="flex: 1; min-height: 500px; resize: vertical; padding: 15px; font-family: monospace;"></textarea>
                <div id="preview" style="flex: 1; padding: 15px; background: #fff; border: 1px solid #ddd; border-radius: 4px; overflow-y: auto; max-height: 500px; font-family: 'Noto Serif SC', serif;"></div>
            </div>
            <script>
                document.getElementById('content').addEventListener('input', function(e) {
                    document.getElementById('preview').innerHTML = marked.parse(e.target.value);
                });
            </script>'''
admin_html = re.sub(old_textarea, new_editor, admin_html)

# Update HTML generation logic
# From: const contentHtml = content.split('\\n').filter(p => p.trim() !== '').map(p => <p></p>).join('');
# To: const contentHtml = marked.parse(content);
admin_html = re.sub(r'const contentHtml = content\.split.*?;', 'const contentHtml = marked.parse(content);', admin_html)

with open('d:/article-sharing-site/admin-article.html', 'w', encoding='utf-8') as f:
    f.write(admin_html)

