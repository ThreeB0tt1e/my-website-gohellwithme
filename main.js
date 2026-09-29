document.documentElement.classList.add('js-enabled');
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

// === 1. 深夜模式无缝切换 ===
(function initTheme() {
    const savedTheme = localStorage.getItem('theme');
    const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
    if (savedTheme === 'dark' || (!savedTheme && prefersDark)) {
        document.documentElement.setAttribute('data-theme', 'dark');
    }
    
    // 在导航栏里插入切换按钮 (非首页)
    const navContainer = document.querySelector('.nav-container');
    if (navContainer && !document.querySelector('.landing-page')) {
        const themeBtn = document.createElement('button');
        themeBtn.id = 'theme-toggle';
        themeBtn.title = '切换深夜模式';
        // 初始图标
        const isDark = document.documentElement.getAttribute('data-theme') === 'dark';
        themeBtn.innerHTML = isDark ? '🌙' : '☀️';
        
        // 放到导航栏的右侧 (汉堡按钮旁边)
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

// === 2. 丝滑转场与呼吸感动画 ===
document.addEventListener('DOMContentLoaded', () => {
    // 监听元素进入视口，给卡片和文章内容加上 visible 类
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('visible');
                // 可选：如果只想触发一次，触发后就取消观察
                observer.unobserve(entry.target);
            }
        });
    }, {
        threshold: 0.1 // 露出 10% 就触发
    });

    const elementsToAnimate = document.querySelectorAll('.card, .article-content, .reader-submit-box, .comments-section');
    elementsToAnimate.forEach(el => observer.observe(el));
});

// === 3. 隐藏的环境音/音乐彩蛋 ===
document.addEventListener('DOMContentLoaded', () => {
    // 仅在首页显示音乐播放按钮，或者全站显示都可以。这里设置为全站显示左下角彩蛋
    const musicBtn = document.createElement('button');
    musicBtn.id = 'music-toggle';
    musicBtn.title = '播放环境音 (请确保网站根目录有 bgm.mp3)';
    musicBtn.innerHTML = '🎵';
    document.body.appendChild(musicBtn);

    const audio = document.createElement('audio');
    audio.id = 'bgm';
    audio.loop = true;
    audio.src = 'bgm.mp3'; // 需要用户自己在文件夹放一个 bgm.mp3
    document.body.appendChild(audio);

    musicBtn.addEventListener('click', () => {
        if (audio.paused) {
            audio.play().then(() => {
                musicBtn.classList.add('playing');
                musicBtn.innerHTML = '🎶';
            }).catch(e => {
                console.error("播放失败，可能是没有 bgm.mp3 文件", e);
                alert("播放失败。如果你想听到音乐，请在 D:\\article-sharing-site 文件夹里放一个名为 'bgm.mp3' 的音乐文件！");
            });
        } else {
            audio.pause();
            musicBtn.classList.remove('playing');
            musicBtn.innerHTML = '🎵';
        }
    });
});

