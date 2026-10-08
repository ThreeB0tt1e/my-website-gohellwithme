import os
import re
import time

directory = 'd:/article-sharing-site'
timestamp = int(time.time())

scripts_to_inject = '''
    <script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.2/gsap.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.2/ScrollTrigger.min.js"></script>
    <script src="https://unpkg.com/split-type"></script>
'''

for filename in os.listdir(directory):
    if filename.endswith('.html'):
        filepath = os.path.join(directory, filename)
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Inject GSAP if not present
        if 'gsap.min.js' not in content:
            content = re.sub(r'<script src="main\.js.*?</script>', scripts_to_inject + r'\g<0>', content)
            
        # Update cache bust
        content = re.sub(r'href="styles\.css(\?v=\d+)?"', f'href="styles.css?v={timestamp}"', content)
        content = re.sub(r'src="main\.js(\?v=\d+)?"', f'src="main.js?v={timestamp}"', content)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)

# Now update styles.css to prevent FOUC (Flash of Unstyled Content)
css_addition = '''
/* =========================================
   Awwwards Quality: Reveal & Parallax
   ========================================= */
/* 防止动画加载前闪烁 */
.awwwards-reveal {
    opacity: 0;
}
.split-line {
    overflow: hidden;
}
'''
with open(os.path.join(directory, 'styles.css'), 'a', encoding='utf-8') as f:
    f.write(css_addition)

# Now add GSAP animation logic to main.js
js_addition = '''
// === Awwwards 品质: 遮罩揭示与视差排版 ===
document.addEventListener('DOMContentLoaded', () => {
    // 确保依赖加载完毕
    if (typeof gsap === 'undefined' || typeof ScrollTrigger === 'undefined' || typeof SplitType === 'undefined') {
        console.warn("Awwwards animation libraries not loaded.");
        return;
    }

    gsap.registerPlugin(ScrollTrigger);

    // 1. 文字遮罩揭示 (Text Mask Reveal)
    // 选定所有大标题和重要的第一段文字
    const revealTargets = document.querySelectorAll('h1, .article-header h1, .book-cover h1, .hero-content h1');
    
    revealTargets.forEach(target => {
        // 先确保元素可见
        target.style.opacity = 1;
        
        // 使用 SplitType 把文字按行切分
        const text = new SplitType(target, { types: 'lines', lineClass: 'split-line-inner' });
        
        // 为每一行包裹一个溢出隐藏的遮罩盒 (Mask)
        text.lines.forEach(line => {
            const wrapper = document.createElement('div');
            wrapper.className = 'split-line';
            line.parentNode.insertBefore(wrapper, line);
            wrapper.appendChild(line);
        });

        // GSAP 动画：从缝隙中抽出的效果
        gsap.from(text.lines, {
            y: '100%',     // 从下方被遮挡的地方开始
            opacity: 0,
            duration: 1.2,
            stagger: 0.1,  // 每一行依次出现
            ease: 'power4.out',
            scrollTrigger: {
                trigger: target,
                start: 'top 85%', // 滚动到屏幕 85% 时触发
                toggleActions: 'play none none none'
            }
        });
    });

    // 为文章正文做轻微的上浮揭示
    const paragraphs = document.querySelectorAll('.article-content > p');
    paragraphs.forEach(p => {
        gsap.from(p, {
            y: 30,
            opacity: 0,
            duration: 1,
            ease: 'power3.out',
            scrollTrigger: {
                trigger: p,
                start: 'top 90%',
            }
        });
    });

    // 2. 微视差排版 (Micro Parallax)
    // 给所有卡片、章节目录加一点视差滚动时间差
    const cards = document.querySelectorAll('.card, .chapter-item');
    cards.forEach((card, index) => {
        gsap.to(card, {
            y: -20, // 向上偏移，产生错落感
            ease: 'none',
            scrollTrigger: {
                trigger: card,
                start: 'top bottom', // 进入视口时开始
                end: 'bottom top',   // 离开视口时结束
                scrub: 0.5 // 平滑挂载在滚动条上
            }
        });
    });
    
    // 给一些背景图或者屏风做更大幅度的视差
    const heros = document.querySelectorAll('.hero, .book-cover');
    heros.forEach(hero => {
        gsap.to(hero, {
            y: 50,
            opacity: 0.5,
            ease: 'none',
            scrollTrigger: {
                trigger: hero,
                start: 'top top',
                end: 'bottom top',
                scrub: true
            }
        });
    });
});
'''
with open(os.path.join(directory, 'main.js'), 'a', encoding='utf-8') as f:
    f.write(js_addition)