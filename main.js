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
    musicBtn.title = '播放环境音 (请确保网站根目录有 bgm.m4a)';
    musicBtn.innerHTML = '🎵';
    document.body.appendChild(musicBtn);

    const audio = document.createElement('audio');
    audio.id = 'bgm';
    audio.loop = true;
    audio.src = 'bgm.m4a';
    document.body.appendChild(audio);

    musicBtn.addEventListener('click', () => {
        if (audio.paused) {
            audio.play().then(() => {
                musicBtn.classList.add('playing');
                musicBtn.innerHTML = '🎶';
            }).catch(e => {
                alert("播放失败。如果你想听到音乐，请在 D:\\article-sharing-site 文件夹里放一个名为 'bgm.m4a' 的音乐文件！");
            });
        } else {
            audio.pause();
            musicBtn.classList.remove('playing');
            musicBtn.innerHTML = '🎵';
        }
    });
});



// === 沉浸式约束：线香阅读进度条 (The Reading Thread) ===
document.addEventListener('DOMContentLoaded', () => {
    // 创建线香 DOM
    const progressContainer = document.createElement('div');
    progressContainer.id = 'reading-progress-container';
    
    const progressThread = document.createElement('div');
    progressThread.id = 'reading-progress-thread';
    
    progressContainer.appendChild(progressThread);
    document.body.appendChild(progressContainer);

    // 监听滚动事件，燃烧线香
    window.addEventListener('scroll', () => {
        const scrollTop = document.documentElement.scrollTop || document.body.scrollTop;
        // 页面总可滚动高度
        const scrollHeight = document.documentElement.scrollHeight - document.documentElement.clientHeight;
        
        if (scrollHeight > 0) {
            const progress = (scrollTop / scrollHeight) * 100;
            progressThread.style.width = progress + '%';
        } else {
            progressThread.style.width = '0%';
        }
    });
});

// === 移动端导航栏切换 ===
document.addEventListener('DOMContentLoaded', () => {
    const navToggle = document.querySelector('.nav-toggle');
    const navLinks = document.querySelector('.nav-links');
    
    if (navToggle && navLinks) {
        navToggle.addEventListener('click', (e) => {
            e.stopPropagation();
            navLinks.classList.toggle('show');
            navToggle.classList.toggle('active');
        });

        // 点击空白处关闭菜单
        document.addEventListener('click', (e) => {
            if (navLinks.classList.contains('show') && !navToggle.contains(e.target) && !navLinks.contains(e.target)) {
                navLinks.classList.remove('show');
                navToggle.classList.remove('active');
            }
        });
    }
});


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

// === 情绪的实体化：一键生成“金句长图” (Quote to Image) ===
document.addEventListener('DOMContentLoaded', () => {
    const isArticlePage = document.querySelector('.article-content');
    if (!isArticlePage) return; // 只在文章页面启用

    // 1. 动态加载 html2canvas
    const script = document.createElement('script');
    script.src = "https://cdn.jsdelivr.net/npm/html2canvas@1.4.1/dist/html2canvas.min.js";
    document.head.appendChild(script);

    // 2. 创建触发按钮 (悬浮在底部)
    const triggerBtn = document.createElement('button');
    triggerBtn.innerText = "生成金句书签";
    triggerBtn.style.cssText = "position: fixed; bottom: 30px; left: 50%; transform: translateX(-50%) translateY(100px); background: #111827; color: #fff; padding: 12px 24px; border-radius: 40px; font-family: 'Noto Serif SC', serif; font-size: 0.9rem; border: none; box-shadow: 0 4px 12px rgba(0,0,0,0.15); opacity: 0; transition: all 0.3s ease; z-index: 10000; cursor: pointer; pointer-events: none;";
    document.body.appendChild(triggerBtn);

    // 3. 监听文字选中
    let selectedQuote = "";
    const handleSelection = () => {
        setTimeout(() => {
            const sel = window.getSelection();
            const text = sel.toString().trim();
            if (sel.rangeCount > 0 && text.length > 0 && text.length < 400) {
                let container = sel.getRangeAt(0).commonAncestorContainer;
                if (container.nodeType !== 1) container = container.parentNode;
                
                // 确保是在正文里选中的
                if (container.closest('.article-content')) {
                    selectedQuote = text;
                    triggerBtn.style.transform = "translateX(-50%) translateY(0)";
                    triggerBtn.style.opacity = "1";
                    triggerBtn.style.pointerEvents = "auto";
                    return;
                }
            }
            triggerBtn.style.transform = "translateX(-50%) translateY(100px)";
            triggerBtn.style.opacity = "0";
            triggerBtn.style.pointerEvents = "none";
        }, 100);
    };

    document.addEventListener('mouseup', handleSelection);
    document.addEventListener('touchend', handleSelection);

    // 4. 构建书签 Modal
    const modal = document.createElement('div');
    modal.style.cssText = "position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.8); z-index: 100000; display: none; flex-direction: column; align-items: center; justify-content: center; overflow-y: auto; padding: 20px;";
    
    // 为了防止截屏时像素模糊，我们把卡片放大多倍，再用 CSS 缩放显示
    const cardScale = 2; // 用2倍率渲染保证清晰度
    modal.innerHTML = 
        <div id="bookmark-card-container" style="position: relative; width: 340px; margin: 20px auto; background: #fff; box-shadow: 0 10px 30px rgba(0,0,0,0.5);">
            <!-- 实际渲染的超清 DOM -->
            <div id="bookmark-card" style="width: \px; padding: \px; background: #fff; position: relative; overflow: hidden; transform: scale(\); transform-origin: top left; margin-bottom: -\px;">
                <div id="bookmark-bg" style="position: absolute; top:0; left:0; width:100%; height:100%; background-size: cover; background-position: center; opacity: 0; transition: opacity 0.3s;"></div>
                <div id="bookmark-overlay" style="position: absolute; top:0; left:0; width:100%; height:100%; background: rgba(255,255,255,0); transition: background 0.3s;"></div>
                
                <div style="position: relative; z-index: 10;">
                    <div style="font-family: 'Playfair Display', serif; font-size: em; color: #e5e7eb; line-height: 1; margin-bottom: -\px;">“</div>
                    <div id="bookmark-quote-text" style="font-size: em; line-height: 2; color: #111827; margin-bottom: \px; font-family: 'Noto Serif SC', serif; white-space: pre-wrap; word-break: break-all; letter-spacing: 1px;"></div>
                    
                    <div style="display: flex; justify-content: space-between; align-items: flex-end; border-top: \px solid #e5e7eb; padding-top: \px;">
                        <div style="font-size: em; color: #4b5563; font-family: 'Noto Serif SC', serif;">
                            <span style="display: block; font-weight: bold; margin-bottom: \px;">《<span id="bookmark-article-title"></span>》</span>
                            <span style="font-family: 'Playfair Display', serif; font-size: em;">Empathy.</span>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        
        <div style="display: flex; gap: 15px; margin-top: 30px; width: 340px; z-index: 20;">
            <label style="flex: 1; background: #fff; color: #111827; text-align: center; padding: 12px; border-radius: 8px; font-family: 'Noto Serif SC', serif; font-size: 0.9rem; cursor: pointer;">
                自定义配图
                <input type="file" id="bookmark-upload" accept="image/*" style="display: none;">
            </label>
            <button id="bookmark-pure" style="flex: 1; background: #f3f4f6; color: #4b5563; border: none; text-align: center; padding: 12px; border-radius: 8px; font-family: 'Noto Serif SC', serif; font-size: 0.9rem; cursor: pointer;">纯文字</button>
        </div>
        <button id="bookmark-save" style="margin-top: 15px; width: 340px; background: #111827; color: #fff; border: none; text-align: center; padding: 14px; border-radius: 8px; font-family: 'Noto Serif SC', serif; font-size: 1rem; cursor: pointer; z-index: 20;">保存书签到相册</button>
        <button id="bookmark-close" style="margin-top: 15px; background: transparent; color: #fff; border: none; opacity: 0.6; font-size: 0.9rem; cursor: pointer; z-index: 20;">取消</button>
    ;
    document.body.appendChild(modal);

    // 5. 事件绑定
    triggerBtn.addEventListener('click', () => {
        window.getSelection().removeAllRanges(); // 取消选中状态
        triggerBtn.style.opacity = "0";
        triggerBtn.style.pointerEvents = "none";
        
        document.getElementById('bookmark-quote-text').innerText = selectedQuote;
        const h1 = document.querySelector('.article-header h1, header h1');
        document.getElementById('bookmark-article-title').innerText = h1 ? h1.innerText : "文章";
        
        modal.style.display = "flex";
        
        // Fix height scale issue
        const card = document.getElementById('bookmark-card');
        const cardContainer = document.getElementById('bookmark-card-container');
        cardContainer.style.height = (card.offsetHeight / cardScale) + 'px';
    });

    document.getElementById('bookmark-close').addEventListener('click', () => {
        modal.style.display = "none";
        document.getElementById('bookmark-bg').style.opacity = "0";
        document.getElementById('bookmark-overlay').style.background = "rgba(255,255,255,0)";
        document.getElementById('bookmark-upload').value = "";
    });

    document.getElementById('bookmark-pure').addEventListener('click', () => {
        document.getElementById('bookmark-bg').style.opacity = "0";
        document.getElementById('bookmark-overlay').style.background = "rgba(255,255,255,0)";
        document.getElementById('bookmark-upload').value = "";
    });

    document.getElementById('bookmark-upload').addEventListener('change', (e) => {
        const file = e.target.files[0];
        if (file) {
            const reader = new FileReader();
            reader.onload = function(event) {
                document.getElementById('bookmark-bg').style.backgroundImage = url(\);
                document.getElementById('bookmark-bg').style.opacity = "1";
                // 加一个白雾遮罩，让黑字依然能看清
                document.getElementById('bookmark-overlay').style.background = "rgba(255,255,255,0.75)";
            }
            reader.readAsDataURL(file);
        }
    });

    document.getElementById('bookmark-save').addEventListener('click', () => {
        const saveBtn = document.getElementById('bookmark-save');
        const originalText = saveBtn.innerText;
        saveBtn.innerText = "生成中...";
        saveBtn.style.opacity = "0.7";
        
        // 修正 html2canvas 滚动偏移 bug
        window.scrollTo(0,0);
        
        html2canvas(document.getElementById('bookmark-card'), {
            scale: 1, // 我们已经用 CSS 放大了内部元素，这里保持 1
            useCORS: true,
            backgroundColor: "#ffffff"
        }).then(canvas => {
            const imgData = canvas.toDataURL('image/png');
            const link = document.createElement('a');
            link.download = Empathy-书签.png;
            link.href = imgData;
            link.click();
            
            saveBtn.innerText = "已保存";
            saveBtn.style.background = "#059669"; // 绿色
            setTimeout(() => {
                saveBtn.innerText = originalText;
                saveBtn.style.background = "#111827";
                saveBtn.style.opacity = "1";
            }, 2000);
        }).catch(err => {
            alert("生成失败，请重试");
            saveBtn.innerText = originalText;
            saveBtn.style.opacity = "1";
        });
    });
});
