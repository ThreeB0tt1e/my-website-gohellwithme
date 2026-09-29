import re

with open('styles.css', 'r', encoding='utf-8') as f:
    css = f.read()

# We want to replace the entire folding screen CSS section
# from "/* =========================================" 
# up to before "/* =========================================" of the next section

start_marker = "/* =========================================\n   🎞️ 宫二屏风分类"
end_marker = "/* =========================================\n   章节列表"

if start_marker in css and end_marker in css:
    pre = css.split(start_marker)[0]
    post = end_marker + css.split(end_marker, 1)[1]
    
    new_css = '''/* =========================================
   🎞️ 宫二屏风分类 (极致轻盈版)
   ========================================= */
.gong-er-quote {
    text-align: center;
    font-family: 'Playfair Display', "Noto Serif SC", serif;
    font-style: italic;
    color: var(--text-muted);
    font-size: 1.1rem;
    margin: 20px 0 60px;
    letter-spacing: 2px;
}

.folding-screen-container {
    display: flex;
    width: 100%;
    height: 55vh;
    min-height: 400px;
    gap: 0;
    margin-bottom: 60px;
    /* 去除所有粗重边框，只留上下极细的分割线 */
    border-top: 1px solid rgba(0,0,0,0.05);
    border-bottom: 1px solid rgba(0,0,0,0.05);
    background: transparent;
}

[data-theme="dark"] .folding-screen-container {
    border-top: 1px solid rgba(255,255,255,0.05);
    border-bottom: 1px solid rgba(255,255,255,0.05);
}

.screen-panel {
    flex: 1;
    background: transparent;
    border-right: 1px solid rgba(0,0,0,0.05);
    position: relative;
    cursor: pointer;
    transition: flex 0.8s cubic-bezier(0.25, 1, 0.5, 1);
    display: flex;
    align-items: center;
    justify-content: center;
    overflow: hidden;
}

[data-theme="dark"] .screen-panel {
    border-right: 1px solid rgba(255,255,255,0.05);
}

.screen-panel:last-child {
    border-right: none;
}

/* 竖排大字 */
.panel-title {
    writing-mode: vertical-rl;
    text-orientation: upright;
    font-size: 2.2rem;
    letter-spacing: 0.5em;
    font-family: "Noto Serif SC", serif;
    color: var(--text-color);
    transition: all 0.8s cubic-bezier(0.25, 1, 0.5, 1);
    margin: 0;
    opacity: 0.8;
}

/* 内部按钮选项 */
.panel-options {
    position: absolute;
    display: flex;
    flex-direction: column;
    gap: 30px;
    opacity: 0;
    transform: translateX(20px);
    transition: all 0.6s ease;
    pointer-events: none;
    z-index: 2;
    left: 50%;
}

/* 悬停/点击展开时的动画 */
.screen-panel:hover, .screen-panel.active {
    flex: 3;
}

.screen-panel:hover .panel-title, .screen-panel.active .panel-title {
    opacity: 0.08; /* 化作淡淡的水印背景 */
    transform: translateX(-120px) scale(2);
}

.screen-panel:hover .panel-options, .screen-panel.active .panel-options {
    opacity: 1;
    transform: translateX(-30px); /* 和左边的水印文字呼应 */
    pointer-events: auto;
    transition-delay: 0.1s;
}

.panel-options .filter-btn {
    background: transparent;
    border: none;
    border-bottom: 1px solid rgba(0,0,0,0.1);
    color: var(--text-muted);
    padding: 5px 0 15px 0;
    font-size: 1.1rem;
    cursor: pointer;
    transition: all 0.4s ease;
    font-family: "Noto Serif SC", serif;
    letter-spacing: 2px;
    text-align: center;
    width: 120px;
}

[data-theme="dark"] .panel-options .filter-btn {
    border-bottom: 1px solid rgba(255,255,255,0.1);
}

.panel-options .filter-btn:hover {
    color: var(--text-color);
    border-bottom-color: var(--text-color);
}

/* 移除旧的 unfolded folded */
'''
    
    # We also need to strip out the previous "屏风扇骨动画" we added
    post = re.sub(r'/\* =========================================\n   屏风扇骨动画.*?}\n', '', post, flags=re.DOTALL)
    
    with open('styles.css', 'w', encoding='utf-8') as f:
        f.write(pre + new_css + '\n' + post)
        
