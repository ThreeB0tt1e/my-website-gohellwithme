$htmlFiles = Get-ChildItem -Path "d:\article-sharing-site\*.html" -Exclude "admin.html"

$toggleHtml = @"
            <button class="nav-toggle" aria-label="Toggle Navigation">
                <span></span>
                <span></span>
                <span></span>
            </button>
            <div class="nav-links">
"@

$scriptHtml = @"
    <script>
        // 手机端导航栏切换逻辑
        const navToggle = document.querySelector('.nav-toggle');
        const navLinks = document.querySelector('.nav-links');
        if (navToggle) {
            navToggle.addEventListener('click', () => {
                navLinks.classList.toggle('show');
                navToggle.classList.toggle('active');
            });
        }
    </script>
</body>
"@

foreach ($file in $htmlFiles) {
    $content = Get-Content $file.FullName -Raw -Encoding UTF8
    
    $modified = $false
    
    # Inject toggle button if not already there
    if ($content -match '<div class="nav-links">' -and $content -notmatch 'nav-toggle') {
        $content = $content -replace '<div class="nav-links">', $toggleHtml
        $modified = $true
    }
    
    # Inject script if not already there
    if ($content -notmatch 'navToggle.addEventListener') {
        $content = $content -replace '</body>', $scriptHtml
        $modified = $true
    }
    
    if ($modified) {
        Set-Content -Path $file.FullName -Value $content -Encoding UTF8
        Write-Host "Updated $($file.Name)"
    }
}
