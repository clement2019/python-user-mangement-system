import sqlite3
from flask import Flask, render_template
from flask import Flask, render_template, request, url_for, flash, redirect,abort

# ...
app = Flask(__name__)
app.config['SECRET_KEY'] = 'your secret key'

def get_db_connection():
    conn = sqlite3.connect('data.db')
    conn.row_factory = sqlite3.Row
    return conn

# ...

@app.route('/new/', methods=('GET', 'POST'))
def new():
    return render_template('create.html')

@app.route('/')
def index():
    conn = get_db_connection()
    posts = conn.execute('SELECT * FROM userpost').fetchall()
    conn.close()
    return render_template('index.html', posts=posts)

# ...

def get_post(post_id):
    conn = get_db_connection()
    post = conn.execute('SELECT * FROM userpost WHERE id = ?',
                        (post_id,)).fetchone()
    conn.close()
    if post is None:
        abort(404)
    return post

# ...

@app.route('/<int:id>/edit/', methods=('GET', 'POST'))
def edit(id):
    post = get_post(id)

    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        if not title:
            flash('Title is required!')

        elif not content:
            flash('Content is required!')

        else:
            conn = get_db_connection()
            conn.execute('UPDATE userpost SET title = ?, content = ?'
                         ' WHERE id = ?',
                         (title, content, id))
            conn.commit()
            conn.close()
            return redirect(url_for('index'))

    return render_template('edit.html', post=post)


@app.route('/create/', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        if not title:
            flash('Title is required!')
        elif not content:
            flash('Content is required!')
        else:
            conn = get_db_connection()
            conn.execute('INSERT INTO userpost (title, content) VALUES (?, ?)',
                         (title, content))
            conn.commit()
            conn.close()
            return redirect(url_for('index'))

    return render_template('create.html')


# ...

@app.route('/<int:id>/delete/', methods=('POST',))
def delete(id):
    post = get_post(id)
    conn = get_db_connection()
    conn.execute('DELETE FROM userpost WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    flash('"{}" was delted successfully !'.format(post['title']))
    return redirect(url_for('index'))


if __name__ == '__main__':
      
       app.run(debug = True)
