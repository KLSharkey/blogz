from flask import Flask, request, redirect, render_template, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blogz:password@localhost:8889/blogz'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
app.secret_key = "246Pass642"


class Blog(db.Model):   #builds class for blog objects

    id = db.Column(db.Integer, primary_key=True) #prim key to differentiate blog posts
    title = db.Column(db.String(120))
    body = db.Column(db.String(500))
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id')) #connects Blog class to User class

    def __init__(self, title, body, username): #initialize blog objects
        self.title = title
        self.body = body
        self.username = username #who the blog belongs to

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True) #prim key to differentiate blog posts
    username = db.Column(db.String(30))
    password = db.Column(db.String(30))
    blogs = db.relationship('Blog', backref='username' ) #builds relat. between User and Blog

    def __init__(self, username, password):
        self.username = username
        self.password = password

@app.before_request  #special handler to run first!
def require_login():
    allowed_routes = ['login','signup', 'index'] #user doesn't have to login to see these
    if request.endpoint not in allowed_routes and 'username' not in session and '/static/' not in request.path: #if there is not a key called email in the session
        return redirect('/login') #push unlogged users to login page




@app.route('/', methods=['POST', 'GET'])
def index():
    users = User.query.all()
    #usernames = users.username
    #print(users.username)
    return render_template('index.html', users=users)
    

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username'] #get username/pass
        password = request.form['password']
        user=User.query.filter_by(username=username).first() #check if username in use yet
        if username and password == user.password: #if username in db and pass correct...
            session['username'] = username #starts session
            return redirect('/newpost') #redirect to blog page
        elif not username:
            flash("Username not yet registered", 'error')
            return redirect('/login')
        else: 
            flash('Incorrect password', 'error')
            return redirect('/login')
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    del session['username']
    return redirect('/blog')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST': #is user signing up
        username=request.form['username']
        password=request.form['password']
        verify=request.form['verify']
        current_users = User.query.filter_by(username = username).first()
        if password == '':
            flash('Please enter a password', 'error')
            return redirect('/signup')
        if username == '':
            flash('Please enter a username', 'error')
            return redirect('/signup')
        if password != verify:
            flash("Password and verify password don't match", 'error')
            return redirect('/signup')
        if len(password) < 3:
            flash("Password must be at least 3 characters long", 'error')
            return redirect('/signup')
        if len(username) < 3:
            flash("Password must be at least 3 characters long", 'error')
            return redirect('/signup')
        if current_users != None:
            if username in current_users:
                flash("Duplicate user", 'error')
                return redirect('/signup')
        else:
            new_user=User(username, password)
            db.session.add(new_user)
            db.session.commit()
            session['username'] = username
            return redirect('/blog')
            
    
    return render_template('signup.html')
        


@app.route('/blog', methods=['POST', 'GET'])  #main/home page for blog. Displays all blog posts
def blog(blog_id=None):
    blogs = Blog.query.all()
    blog_id = request.args.get('id')
    #owner_id = request.form['owner_id']
    #blog_info = Blog.query.all()
    #owners_info = User.query.all()
    #print(owners_info)
    user_id = request.args.get('owner')
    #user_name = User.query.filter_by()
    users = User.query.all()
    
    if blog_id == None and user_id == None: #if blog not chosen, display all blogs in list
        return render_template('blog.html', blogs=blogs, users=users)


    blog_id = request.args.get('id') #get blog id
    if blog_id != None: #if blog chosen, display it in blog entry
        blog=Blog.query.get(blog_id)
        blog_info = Blog.query.filter_by(id = blog_id).first()
        #user_blogs = Blog.query.filter_by(owner_id = user_id).all()
        user_name = User.query.filter_by(id=blog.owner_id).first()
        
        return render_template('blog_entry.html', blog=blog)

    #user_id = request.args.get('owner') #get owner id
    print(user_id)
    if user_id != None:
        #blogs = Blog.query.get(user_id)
        user_blogs = Blog.query.filter_by(owner_id = user_id).all()
        user_name = User.query.filter_by(id=user_id).first()
        return render_template('singleUser.html', user_blogs=user_blogs, user_name=user_name)

@app.route('/newpost', methods=['POST', 'GET']) #where you create blogs with title and body
def newpost():
    title_error = ''
    body_error = ''
    if request.method == 'POST':
        make_title = request.form['title'] #gets title from form on /newpost
        make_body = request.form['body'] #gets body from form on /newpost
        owner = User.query.filter_by(username=session['username']).first()
        
        if make_body == '':
            body_error = "Please give a title" #defining errors
        if make_title == '':
            title_error = "Please enter text into the body"
        
        if title_error=='' and body_error=='':    
            new_blog = Blog(make_title, make_body, owner)
            
            db.session.add(new_blog)  #adds and commits both title and body to the database 
            db.session.commit()
            
            blog_id=new_blog.id
            owner = session.get('username')
           
            return redirect(url_for('blog', id=blog_id, owner=owner)) #direct to new post made after creation
            #return redirect(url_for('blog_entry', id=new_blog.id))
        else:
            return render_template("newpost.html", title_error=title_error, body_error=body_error) #if error, re-render newpost page with errors

    else:
        
        return render_template('newpost.html') #displays new post form and sends it title and body

    
if __name__ == '__main__': #run app
    app.run()