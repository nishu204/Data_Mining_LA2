from flask import Flask, render_template, request
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

def get_links(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        links = [a.get('href') for a in soup.find_all('a', href=True)]
        return links
    except Exception as e:
        return []

def dfs_crawler(seed_url, max_depth, visited, current_depth):
    if current_depth > max_depth:
        return []

    links = get_links(seed_url)
    visited.add(seed_url)

    result = [{'url': seed_url, 'depth': current_depth, 'links': links}]

    for link in links:
        if link not in visited:
            result.extend(dfs_crawler(link, max_depth, visited, current_depth + 1))

    return result

def bfs_crawler(seed_url, max_depth):
    visited = set()
    queue = [(seed_url, 0)]

    result = []

    while queue:
        current_url, current_depth = queue.pop(0)

        if current_depth > max_depth:
            continue

        if current_url not in visited:
            links = get_links(current_url)
            visited.add(current_url)
            result.append({'url': current_url, 'depth': current_depth, 'links': links})

            for link in links:
                queue.append((link, current_depth + 1))

    return result

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/crawl', methods=['POST'])
def crawl():
    seed_url = request.form['seed_url']
    max_depth = int(request.form['max_depth'])
    algo_type = request.form['algo_type']

    if algo_type == 'dfs':
        result = dfs_crawler(seed_url, max_depth, set(), 0)
    elif algo_type == 'bfs':
        result = bfs_crawler(seed_url, max_depth)
    else:
        result = []

    return render_template('result.html', result=result)

if __name__ == '__main__':
    app.run(debug=True)
