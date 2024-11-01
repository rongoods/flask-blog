import json

from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)


def load_posts():
    with open('blog_posts.json', 'r') as file:
        return json.load(file)


def save_posts(posts):
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
        save_posts(new_post)
        return redirect(url_for('index'))
    return render_template('add.html')


@app.route('/delete/<int:post_id>')
def delete(post_id):
    posts = load_posts()
    updated_posts = [post for post in posts if post['id'] != post_id]

    if len(updated_posts) == len(posts):
        return "Post not found", 404
    save_posts(updated_posts)
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
