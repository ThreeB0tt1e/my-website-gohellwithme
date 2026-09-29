import re

with open('characters.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Change title
content = content.replace('<h1>人物（暂定）</h1>', '<h1>人物介绍（共创版）</h1>')

# Remove subtitle
content = re.sub(r'<p>这里没有预设的评价，每个人物是什么样，交给大家来定义。</p>', '', content)

with open('characters.html', 'w', encoding='utf-8') as f:
    f.write(content)
