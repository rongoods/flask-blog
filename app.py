import json

from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)


def load_posts():
    with open('blog_posts.json', 'r') as file:
        return json.load(file)


def save_post(new_post):
    posts = load_posts()
    posts.append(new_post)
    with open('blog_posts.json', 'w') as file:
        json.dump(posts, file, indent=4)


@app.route('/')
def index():
    blog_posts = load_posts()
    return render_template('index.html', posts=blog_posts)


@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        new_id = len(load_posts()) + 1
        new_post = {
            "id": new_id,
            "author": request.form['author'],
            "title": request.form['title'],
            "content": request.form['content']
        }
        save_post(new_post)
        return redirect(url_for('index'))
    return render_template('add.html')


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
