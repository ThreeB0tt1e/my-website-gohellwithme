document.documentElement.classList.add('js-enabled');

// === 1. 深夜模式无缝切换 ===
(function initTheme() {
    const savedTheme = localStorage.getItem('theme');
    const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
    if (savedTheme === 'dark' || (!savedTheme && prefersDark)) {
        document.documentElement.setAttribute('data-theme', 'dark');
    }
    
    const navContainer = document.querySelector('.nav-container');
    if (navContainer && !document.querySelector('.landing-page')) {
        const themeBtn = document.createElement('button');
        themeBtn.id = 'theme-toggle';
        themeBtn.title = '切换深夜模式';
        const isDark = document.documentElement.getAttribute('data-theme') === 'dark';
        themeBtn.innerHTML = isDark ? '🌙' : '☀️';
        navContainer.appendChild(themeBtn);
        
        themeBtn.addEventListener('click', () => {
            const currentTheme = document.documentElement.getAttribute('data-theme');
            if (currentTheme === 'dark') {
                document.documentElement.removeAttribute('data-theme');
                localStorage.setItem('theme', 'light');
                themeBtn.innerHTML = '☀️';
            } else {
                document.documentElement.setAttribute('data-theme', 'dark');
                localStorage.setItem('theme', 'dark');
                themeBtn.innerHTML = '🌙';
            }
        });
    }
})();

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

    // 3. 上一篇/下一篇 自动导航 (独立连载优化版)
    const articleContent = document.querySelector('.article-content');
    const isArticlePage = articleContent && !window.location.pathname.includes('guestbook') && document.querySelector('.article-header');
    
    if (isArticlePage) {
        let currentPath = window.location.pathname.split('/').pop();
        if (!currentPath) currentPath = 'index.html';
        
        const devilSeries = [
            { href: 'hell.html', title: '序言：魔鬼契约' },
            { href: '2.html', title: '魔鬼契约 2' },
            { href: '3.html', title: '清道夫' },
            { href: '4.html', title: '魔鬼契约 4' },
            { href: '5.html', title: '忍者' },
            { href: 'fanwai.html', title: '番外篇' }
        ];
        
        const devilIndex = devilSeries.findIndex(l => l.href === currentPath);
        
        if (devilIndex !== -1) {
            // 是魔鬼契约连载，走正序逻辑
            const navDiv = document.createElement('div');
            navDiv.className = 'article-nav';
            let html = '';
            
            if (devilIndex > 0) {
                const prev = devilSeries[devilIndex - 1];
                html += <a href=" + prev.href + " class="nav-prev"><span class="arrow">←</span> <span class="title">上一章： + prev.title + </span></a>;
            } else {
                html += <span class="nav-prev empty"></span>;
            }
            
            if (devilIndex < devilSeries.length - 1) {
                const next = devilSeries[devilIndex + 1];
                html += <a href=" + next.href + " class="nav-next"><span class="title">下一章： + next.title + </span> <span class="arrow">→</span></a>;
            } else {
                html += <a href="contract.html" class="nav-next"><span class="title">返回连载目录</span> <span class="arrow">↑</span></a>;
            }
            
            navDiv.innerHTML = html;
            articleContent.appendChild(navDiv);
            
            // 额外给连载添加一个返回目录的浮动按钮
            const tocBtn = document.createElement('a');
            tocBtn.href = 'contract.html';
            tocBtn.id = 'toc-btn';
            tocBtn.title = '返回魔鬼契约目录';
            tocBtn.innerHTML = '≡';
            document.body.appendChild(tocBtn);
            
        } else {
            // 普通文章，走抓取目录的倒序逻辑
            try {
                const response = await fetch('articles.html');
                const text = await response.text();
                const parser = new DOMParser();
                const doc = parser.parseFromString(text, 'text/html');
                
                const links = Array.from(doc.querySelectorAll('.card h2 a')).map(a => ({
                    href: a.getAttribute('href'),
                    title: a.textContent
                }));
                
                const currentIndex = links.findIndex(l => l.href === currentPath);
                
                if (currentIndex !== -1) {
                    const navDiv = document.createElement('div');
                    navDiv.className = 'article-nav';
                    let html = '';
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
    }
});

// === 丝滑转场与呼吸感动画 ===
document.addEventListener('DOMContentLoaded', () => {
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('visible');
                observer.unobserve(entry.target);
            }
        });
    }, { threshold: 0.1 });

    // 包括刚才新增的 chapter-item
    const elementsToAnimate = document.querySelectorAll('.card, .article-content, .reader-submit-box, .comments-section, .chapter-item');
    elementsToAnimate.forEach(el => observer.observe(el));
});

// === 电影级网页过场动画 ===
document.addEventListener('DOMContentLoaded', () => {
    const links = document.querySelectorAll('a[href]');
    links.forEach(link => {
        link.addEventListener('click', (e) => {
            const target = link.getAttribute('href');
            if (
                target.startsWith('http') || 
                target.startsWith('#') || 
                target.startsWith('mailto:') ||
                link.getAttribute('target') === '_blank' ||
                e.ctrlKey || e.metaKey
            ) { return; }
            e.preventDefault();
            document.body.classList.add('page-transitioning-out');
            setTimeout(() => { window.location.href = target; }, 350);
        });
    });
});
window.addEventListener('pageshow', (event) => {
    if (event.persisted || document.body.classList.contains('page-transitioning-out')) {
        document.body.classList.remove('page-transitioning-out');
    }
});

// === 隐藏的环境音/音乐彩蛋 ===
document.addEventListener('DOMContentLoaded', () => {
    const musicBtn = document.createElement('button');
    musicBtn.id = 'music-toggle';
    musicBtn.title = '播放环境音 (请确保网站根目录有 bgm.mp3)';
    musicBtn.innerHTML = '🎵';
    document.body.appendChild(musicBtn);

    const audio = document.createElement('audio');
    audio.id = 'bgm';
    audio.loop = true;
    audio.src = 'bgm.mp3';
    document.body.appendChild(audio);

    musicBtn.addEventListener('click', () => {
        if (audio.paused) {
            audio.play().then(() => {
                musicBtn.classList.add('playing');
                musicBtn.innerHTML = '🎶';
            }).catch(e => {
                alert("播放失败。如果你想听到音乐，请在 D:\\article-sharing-site 文件夹里放一个名为 'bgm.mp3' 的音乐文件！");
            });
        } else {
            audio.pause();
            musicBtn.classList.remove('playing');
            musicBtn.innerHTML = '🎵';
        }
    });
});
