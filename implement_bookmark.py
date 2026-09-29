import os

js_code = '''
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
                    <div style="font-family: 'Playfair Display', serif; font-size: \rem; color: #e5e7eb; line-height: 1; margin-bottom: -\px;">“</div>
                    <div id="bookmark-quote-text" style="font-size: \rem; line-height: 2; color: #111827; margin-bottom: \px; font-family: 'Noto Serif SC', serif; white-space: pre-wrap; word-break: break-all; letter-spacing: 1px;"></div>
                    
                    <div style="display: flex; justify-content: space-between; align-items: flex-end; border-top: \px solid #e5e7eb; padding-top: \px;">
                        <div style="font-size: \rem; color: #4b5563; font-family: 'Noto Serif SC', serif;">
                            <span style="display: block; font-weight: bold; margin-bottom: \px;">《<span id="bookmark-article-title"></span>》</span>
                            <span style="font-family: 'Playfair Display', serif; font-size: \rem;">Empathy.</span>
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
'''

with open('d:/article-sharing-site/main.js', 'a', encoding='utf-8') as f:
    f.write(js_code)
