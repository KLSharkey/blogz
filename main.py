from flask import Flask, request, redirect, render_template, url_for
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
def blog(blog_id=None):
    blogs = Blog.query.all()
    blog_id = request.args.get('id')
    if blog_id == None: #if blog not chosen, display all blogs in list
        return render_template('blog.html', blogs=blogs)


    blog_id = request.args.get('id') #get blog id
    if blog_id != None: #if blog chosen, display it in blog entry
        blog=Blog.query.get(blog_id)
        return render_template('blog_entry.html', blog=blog)

 

@app.route('/newpost', methods=['POST', 'GET']) #where you create blogs with title and body
def newpost():
    title_error = ''
    body_error = ''
    if request.method == 'POST':
        make_title = request.form['title'] #gets title from form on /newpost
        make_body = request.form['body'] #gets body from form on /newpost
        if make_body == '':
            body_error = "Please give a title" #defining errors
        if make_title == '':
            title_error = "Please enter text into the body"
        
        if title_error=='' and body_error=='':    
            new_blog = Blog(make_title, make_body)
            db.session.add(new_blog)  #adds and commits both title and body to the database 
            db.session.commit()
            
            blog_id=new_blog.id
            
            return redirect(url_for('blog', id=blog_id)) #direct to new post made after creation
            #return redirect(url_for('blog_entry', id=new_blog.id))
        else:
            return render_template("newpost.html", title_error=title_error, body_error=body_error) #if error, re-render newpost page with errors

    else:
        
        return render_template('newpost.html') #displays new post form and sends it title and body

    
if __name__ == '__main__': #run app
    app.run()