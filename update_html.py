import re

with open('articles.html', 'r', encoding='utf-8') as f:
    html = f.read()

old_screen = r'<div class="folding-screen-container js-enabled">.*?</div>\s*</div>'
# Wait, the closing tags might be different. Let's just find the whole folding-screen-container block.
pattern = r'<div class="folding-screen-container js-enabled">.*?</div>\s*<div class="article-grid'

new_screen = '''<div class="folding-screen-container js-enabled">
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
                    <button class="filter-btn" onclick="filterCategory('all', this)">全部</button>
                </div>
            </div>
        </div>

        <div class="article-grid'''

html = re.sub(pattern, new_screen, html, flags=re.DOTALL)

# Now fix the javascript
old_script_pattern = r'<script>\s*function filterStage.*?</script>'
new_script = '''<script>
        function filterCategory(cat, btn) {
            // 防止冒泡触发折叠
            if (event) event.stopPropagation();

            const grid = document.querySelector('.article-grid');
            grid.style.display = 'flex';
            
            grid.style.opacity = '0';
            setTimeout(() => {
                document.querySelectorAll('.chapter-item').forEach(article => {
                    if (cat === 'all' || article.getAttribute('data-category') === cat) {
                        article.style.display = 'flex';
                    } else {
                        article.style.display = 'none';
                    }
                });
                grid.style.opacity = '1';
                grid.style.transition = 'opacity 0.8s ease';
            }, 50);
            
            setTimeout(() => {
                grid.scrollIntoView({ behavior: 'smooth', block: 'start' });
            }, 200);
        }
    </script>'''

html = re.sub(old_script_pattern, new_script, html, flags=re.DOTALL)

with open('articles.html', 'w', encoding='utf-8') as f:
    f.write(html)
