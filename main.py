from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:klwwlk@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)


class Blog(db.Model):   #builds class for blog objects

    id = db.Column(db.Integer, primary_key=True) #prim key to differentiate blog posts
    title = db.Column(db.String(120))
    body = db.Column(db.String(500))

    def __init__(self, title, body): #initialize blog objects
        self.title = title
        self.body = body


@app.route('/blog', methods=['POST', 'GET'])  #main/home page for blog. Displays all blog posts
def blog():
    blogs = Blog.query.all()

    #title = request.form['title'] #gets title from form on /newpost
    #body = request.form['body'] #gets body from form on /newpost
    return render_template('blog.html', blogs=blogs)

 

@app.route('/newpost', methods=['POST', 'GET']) #where you create blogs with title and body
def newpost():
    if request.method == 'POST':
        make_title = request.form['title'] #gets title from form on /newpost
        #new_title = Blog(make_titl)
        make_body = request.form['body'] #gets body from form on /newpost
        new_blog = Blog(make_title, make_body)
        db.session.add(new_blog)  #adds and commits both title and body to the database 
        #db.session.add(new_body)
        db.session.commit()
        return redirect('/blog')

    else:
    #body = blog.query.filter_by().all()
        return render_template('newpost.html') #displays new post form and sends it title and body
  


    
if __name__ == '__main__': #run app
    app.run()