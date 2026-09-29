from bs4 import BeautifulSoup

with open('articles.html', 'r', encoding='utf-8') as f:
    html = f.read()

soup = BeautifulSoup(html, 'html.parser')
grid = soup.find('div', class_='article-grid')
print('Found grid?', grid is not None)
if grid:
    articles = grid.find_all('article', class_='card')
    print('Found articles:', len(articles))
