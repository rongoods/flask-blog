import json

from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)


def load_posts():
    with open('blog_posts.json', 'r') as file:
        return json.load(file)


def save_posts(posts):
    with open('blog_posts.json', 'w') as file:
        json.dump(posts, file, indent=4)


def fetch_post_by_id(post_id):
    posts = load_posts()
    for post in posts:
        if post['id'] == post_id:
            return post
    return None


@app.route('/')
def index():
    blog_posts = load_posts()
    return render_template('index.html', posts=blog_posts)


@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        posts = load_posts()
        new_id = len(posts) + 1
        new_post = {
            "id": new_id,
            "author": request.form['author'],
            "title": request.form['title'],
            "content": request.form['content'],
            "likes": 0
        }
        posts.append(new_post)
        save_posts(posts)
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


@app.route('/update/<int:post_id>', methods=['GET', 'POST'])
def update(post_id):
    post = fetch_post_by_id(post_id)
    if post is None:
        return "Post not found", 404

    if request.method == 'POST':
        post['author'] = request.form['author']
        post['title'] = request.form['title']
        post['content'] = request.form['content']

        posts = load_posts()
        for idx, p in enumerate(posts):
            if p['id'] == post_id:
                posts[idx] = post
                break

        save_posts(posts)
        return redirect(url_for('index'))

    return render_template('update.html', post=post)


@app.route('/like/<int:post_id>', methods=['POST'])
def like(post_id):
    posts = load_posts()
    post = fetch_post_by_id(post_id)

    if post is None:
        return "Post not found", 404

    post['likes'] += 1

    for idx, p in enumerate(posts):
        if p['id'] == post_id:
            posts[idx] = post
            break
    save_posts(posts)
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
