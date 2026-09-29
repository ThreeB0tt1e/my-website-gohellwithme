import re

with open('articles.html', 'r', encoding='utf-8') as f:
    html = f.read()

old_script_pattern = r'<script>\s*const viewScreen.*?function goBackToScreen\(\) \{\s*switchView\(viewCategories, viewScreen\);\s*\}\s*</script>'
new_script = '''<script>
        const viewScreen = document.getElementById('view-screen');
        const viewCategories = document.getElementById('view-categories');
        const viewArticles = document.getElementById('view-articles');
        const catButtonsContainer = document.getElementById('category-buttons');

        // 用户的所有分类，不再受限于哪一扇屏风
        const allCategories = ['今日杂谈', '游记', '寓言', '糖果屋', '魔鬼契约'];

        function switchView(hideEl, showEl, setupCallback) {
            hideEl.style.opacity = '0';
            setTimeout(() => {
                hideEl.style.display = 'none';
                if (setupCallback) setupCallback();
                showEl.style.display = 'flex';
                // Trigger reflow
                void showEl.offsetWidth;
                showEl.style.opacity = '1';
            }, 500);
        }

        function openStage() {
            // 不管点击哪扇门，都打开所有分类。具体什么文章属于“见自己”或“见天地”，由读者在心中自行定义。
            switchView(viewScreen, viewCategories, () => {
                catButtonsContainer.innerHTML = '';
                allCategories.forEach(cat => {
                    const btn = document.createElement('button');
                    btn.className = 'pill-btn';
                    btn.innerText = cat;
                    btn.onclick = () => openCategory(cat);
                    catButtonsContainer.appendChild(btn);
                });
            });
        }

        function openCategory(cat) {
            switchView(viewCategories, viewArticles, () => {
                document.querySelectorAll('.chapter-item').forEach(article => {
                    if (article.getAttribute('data-category') === cat) {
                        article.style.display = 'flex';
                    } else {
                        article.style.display = 'none';
                    }
                });
            });
        }

        function goBackToCategories() {
            switchView(viewArticles, viewCategories);
        }

        function goBackToScreen() {
            switchView(viewCategories, viewScreen);
        }
    </script>'''

html = re.sub(old_script_pattern, new_script, html, flags=re.DOTALL)

# And we also need to change the onclick="openStage('见自己')" to just openStage()
html = re.sub(r'onclick="openStage\(\'[^\']+\'\)"', 'onclick="openStage()"', html)

with open('articles.html', 'w', encoding='utf-8') as f:
    f.write(html)
