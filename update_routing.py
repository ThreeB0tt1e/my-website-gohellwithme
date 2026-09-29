import re

with open('articles.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Replace the script block
old_script = r'<script>\s*const viewScreen.*?function goBackToScreen\(\) \{.*?</script>'

new_script = '''<script>
        const viewScreen = document.getElementById('view-screen');
        const viewCategories = document.getElementById('view-categories');
        const viewArticles = document.getElementById('view-articles');
        const catButtonsContainer = document.getElementById('category-buttons');

        const allCategories = ['今日杂谈', '游记', '寓言', '糖果屋', '魔鬼契约'];

        function switchView(hideEl, showEl, setupCallback) {
            hideEl.style.opacity = '0';
            setTimeout(() => {
                hideEl.style.display = 'none';
                if (setupCallback) setupCallback();
                showEl.style.display = 'flex';
                void showEl.offsetWidth;
                showEl.style.opacity = '1';
            }, 300); // 加快了一点动画速度
        }

        function openStage() {
            window.location.hash = 'categories';
        }

        function openCategory(cat) {
            window.location.hash = 'cat-' + encodeURIComponent(cat);
        }

        function renderCategories() {
            catButtonsContainer.innerHTML = '';
            allCategories.forEach(cat => {
                const btn = document.createElement('button');
                btn.className = 'pill-btn';
                btn.innerText = cat;
                btn.onclick = () => openCategory(cat);
                catButtonsContainer.appendChild(btn);
            });
        }

        function handleHashChange() {
            const hash = window.location.hash;
            
            // 隐藏所有
            viewScreen.style.display = 'none';
            viewCategories.style.display = 'none';
            viewArticles.style.display = 'none';
            
            viewScreen.style.opacity = '0';
            viewCategories.style.opacity = '0';
            viewArticles.style.opacity = '0';

            if (hash.startsWith('#cat-')) {
                const cat = decodeURIComponent(hash.replace('#cat-', ''));
                document.querySelectorAll('.chapter-item').forEach(article => {
                    if (article.getAttribute('data-category') === cat) {
                        article.style.display = 'flex';
                    } else {
                        article.style.display = 'none';
                    }
                });
                viewArticles.style.display = 'flex';
                setTimeout(() => viewArticles.style.opacity = '1', 50);
            } 
            else if (hash === '#categories') {
                renderCategories();
                viewCategories.style.display = 'flex';
                setTimeout(() => viewCategories.style.opacity = '1', 50);
            } 
            else {
                viewScreen.style.display = 'flex';
                setTimeout(() => viewScreen.style.opacity = '1', 50);
            }
        }

        // 监听浏览器前进后退和 Hash 变化
        window.addEventListener('hashchange', handleHashChange);
        
        // 页面加载时执行一次
        document.addEventListener('DOMContentLoaded', handleHashChange);

        function goBackToCategories() {
            window.location.hash = 'categories';
        }

        function goBackToScreen() {
            window.location.hash = '';
        }
    </script>'''

html = re.sub(old_script, new_script, html, flags=re.DOTALL)

# Need to change onclick="openStage()" to just openStage() without any other logic if needed, but it already is.

with open('articles.html', 'w', encoding='utf-8') as f:
    f.write(html)
