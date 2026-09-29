document.addEventListener('DOMContentLoaded', async () => {
    // 1. 回到顶部按钮
    const backToTop = document.createElement('button');
    backToTop.id = 'back-to-top';
    backToTop.innerHTML = '↑';
    backToTop.title = '回到顶部';
    document.body.appendChild(backToTop);

    window.addEventListener('scroll', () => {
        if (window.scrollY > 300) {
            backToTop.classList.add('show');
        } else {
            backToTop.classList.remove('show');
        }
    });

    backToTop.addEventListener('click', () => {
        window.scrollTo({ top: 0, behavior: 'smooth' });
    });

    // 2. 图片放大功能
    if (typeof mediumZoom === 'function') {
        mediumZoom('.article-content img', {
            margin: 24,
            background: 'rgba(255, 255, 255, 0.95)'
        });
    }

    // 3. 上一篇/下一篇 自动导航
    const articleContent = document.querySelector('.article-content');
    // 只有文章详情页才有上一篇/下一篇
    const isArticlePage = articleContent && !window.location.pathname.includes('guestbook') && document.querySelector('.article-header');
    
    if (isArticlePage) {
        try {
            const response = await fetch('articles.html');
            const text = await response.text();
            const parser = new DOMParser();
            const doc = parser.parseFromString(text, 'text/html');
            
            const links = Array.from(doc.querySelectorAll('.card h2 a')).map(a => ({
                href: a.getAttribute('href'),
                title: a.textContent
            }));

            // 获取当前文件名，处理可能的路径参数
            let currentPath = window.location.pathname.split('/').pop();
            if (!currentPath) currentPath = 'index.html';
            
            const currentIndex = links.findIndex(l => l.href === currentPath);
            
            if (currentIndex !== -1) {
                const navDiv = document.createElement('div');
                navDiv.className = 'article-nav';
                
                let html = '';
                // 由于列表是从新到旧排列，所以 index 越小文章越新
                // 常见的逻辑是：上一篇是更新的，下一篇是更旧的
                if (currentIndex > 0) {
                    const prev = links[currentIndex - 1];
                    html += <a href=" + prev.href + " class="nav-prev"><span class="arrow">←</span> <span class="title">上一篇： + prev.title + </span></a>;
                } else {
                    html += <span class="nav-prev empty"></span>;
                }
                
                if (currentIndex < links.length - 1) {
                    const next = links[currentIndex + 1];
                    html += <a href=" + next.href + " class="nav-next"><span class="title">下一篇： + next.title + </span> <span class="arrow">→</span></a>;
                }
                
                navDiv.innerHTML = html;
                articleContent.appendChild(navDiv);
            }
        } catch (e) {
            console.error("Failed to load article navigation", e);
        }
    }
});
