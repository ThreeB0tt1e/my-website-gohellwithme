import os
import re

articles_path = 'd:/article-sharing-site/articles.html'

with open(articles_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Replace the beginning of the DOMContentLoaded script
old_init = "document.addEventListener('DOMContentLoaded', () => {"
new_init = '''document.addEventListener('DOMContentLoaded', () => {
            const canvas = document.getElementById('fog-canvas');
            const overlay = document.getElementById('fog-overlay');
            const hint = document.getElementById('fog-hint');
            const archiveContainer = document.querySelector('.archive-container');
            const archiveItems = document.querySelectorAll('.archive-item');
            
            // Check if user has already cleared the veil this session
            if (sessionStorage.getItem('empathy_veil_cleared') === 'true') {
                if (overlay) overlay.remove();
                if (hint) hint.remove();
                archiveContainer.style.display = 'block';
                // Quick fade in for returning users
                gsap.fromTo(archiveItems, 
                    { y: 20, opacity: 0 },
                    { y: 0, opacity: 1, duration: 0.8, stagger: 0.05, ease: 'power2.out' }
                );
                return; // skip the rest of the canvas logic
            }
'''

# Wait, the best way is just to replace the specific block.
# Let's write a targeted regex or just rewrite the JS block.

js_block = '''<script>
        // === The Canvas Veil Logic ===
        document.addEventListener('DOMContentLoaded', () => {
            const canvas = document.getElementById('fog-canvas');
            const overlay = document.getElementById('fog-overlay');
            const hint = document.getElementById('fog-hint');
            const archiveContainer = document.querySelector('.archive-container');
            const archiveItems = document.querySelectorAll('.archive-item');
            
            // UX: Only require wiping once per session
            if (sessionStorage.getItem('empathy_veil_cleared') === 'true') {
                if (overlay) overlay.remove();
                if (hint) hint.remove();
                archiveContainer.style.display = 'block';
                gsap.fromTo(archiveItems, 
                    { opacity: 0, y: 15 },
                    { opacity: 1, y: 0, duration: 0.6, stagger: 0.05, ease: 'power2.out' }
                );
                return;
            }
            
            if (!canvas) return;
            const ctx = canvas.getContext('2d', { willReadFrequently: true });
            
            let width = window.innerWidth;
            let height = window.innerHeight;
            
            function resize() {
                width = window.innerWidth;
                height = window.innerHeight;
                canvas.width = width;
                canvas.height = height;
                fillFog();
            }
            
            function fillFog() {
                ctx.globalCompositeOperation = 'source-over';
                ctx.fillStyle = '#111827'; // Dark charcoal fog
                ctx.fillRect(0, 0, width, height);
            }
            
            window.addEventListener('resize', resize);
            resize();
            
            archiveContainer.style.display = 'block';
            
            let isDrawing = false;
            let totalErasedPixels = 0;
            let veilRemoved = false;
            let lastPos = null;
            
            function getPos(e) {
                if (e.touches && e.touches.length > 0) {
                    return { x: e.touches[0].clientX, y: e.touches[0].clientY };
                }
                return { x: e.clientX, y: e.clientY };
            }
            
            function erase(x, y) {
                if (veilRemoved) return;
                
                if (lastPos) {
                    const dx = x - lastPos.x;
                    const dy = y - lastPos.y;
                    totalErasedPixels += Math.sqrt(dx*dx + dy*dy);
                }
                lastPos = {x, y};
                
                ctx.globalCompositeOperation = 'destination-out';
                const radius = window.innerWidth < 768 ? 60 : 100;
                const gradient = ctx.createRadialGradient(x, y, 0, x, y, radius);
                gradient.addColorStop(0, 'rgba(0,0,0,1)');
                gradient.addColorStop(0.5, 'rgba(0,0,0,0.8)');
                gradient.addColorStop(1, 'rgba(0,0,0,0)');
                
                ctx.beginPath();
                ctx.fillStyle = gradient;
                ctx.arc(x, y, radius, 0, Math.PI * 2);
                ctx.fill();
                
                const threshold = window.innerWidth < 768 ? 2000 : 4000;
                if (totalErasedPixels > threshold && !veilRemoved) {
                    removeVeil();
                }
            }
            
            function removeVeil() {
                veilRemoved = true;
                overlay.style.pointerEvents = 'none';
                
                // Record that user has cleared it this session
                sessionStorage.setItem('empathy_veil_cleared', 'true');
                
                gsap.to([overlay, hint], {
                    opacity: 0,
                    duration: 1.5,
                    ease: 'power2.inOut',
                    onComplete: () => {
                        overlay.remove();
                        hint.remove();
                    }
                });
                
                gsap.fromTo(archiveItems, 
                    { y: 50, opacity: 0 },
                    { y: 0, opacity: 1, duration: 1.2, stagger: 0.1, ease: 'power3.out', delay: 0.2 }
                );
            }
            
            overlay.addEventListener('mousedown', (e) => { isDrawing = true; lastPos = null; erase(e.clientX, e.clientY); });
            overlay.addEventListener('mousemove', (e) => { if (isDrawing) erase(e.clientX, e.clientY); });
            window.addEventListener('mouseup', () => { isDrawing = false; lastPos = null; });
            
            overlay.addEventListener('touchstart', (e) => { isDrawing = true; lastPos = null; const p = getPos(e); erase(p.x, p.y); });
            overlay.addEventListener('touchmove', (e) => { if (isDrawing) { e.preventDefault(); const p = getPos(e); erase(p.x, p.y); } }, {passive: false});
            window.addEventListener('touchend', () => { isDrawing = false; lastPos = null; });
        });
    </script>
</body>
</html>'''

new_content = re.sub(r'<script>\s*// === The Canvas Veil Logic ===.*</html>', js_block, content, flags=re.DOTALL)

with open(articles_path, 'w', encoding='utf-8') as f:
    f.write(new_content)