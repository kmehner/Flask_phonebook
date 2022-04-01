from app import app
from flask import redirect, render_template, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from app.templates3.forms import AddressForm, SignUpForm, PostForm, LoginForm, SearchForm
from app.templates3.models import User, Address, Post

@app.route('/')
def index():
    title = 'Home'
    posts = Post.query.all()
    return render_template('index.html', title=title, posts=posts)


@app.route('/signup', methods=["GET", "POST"])
def signup():
    title = 'Sign Up'
    form = SignUpForm()
    # check if a post request and that the form is valid
    if form.validate_on_submit():
        # Get data from the validated form
        email = form.email.data
        username = form.username.data
        password = form.password.data
        # Check if there is a user with email or username
        users_with_that_info = User.query.filter((User.username==username)|(User.email==email)).all() 
        if users_with_that_info:
            flash(f"There is already a user with that username and/or email. Please try again", "danger")
            return render_template('signup.html', title=title, form=form)

        # Create a new user instance with form data
        new_user = User(email=email, username=username, password=password)
        # flash message saying new user has been created
        flash(f"{new_user.username} has succesfully signed up.", "success")
        login_user(new_user)
        return redirect(url_for('index'))

    return render_template('signup.html', title=title, form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    title = 'Log In'
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        # Query for a user with that username
        user = User.query.filter_by(username=username).first()
        # Check if there is a user and the password is correct
        if user and user.check_password(password):
            # log the user in with flask-login
            login_user(user)
            # flash message that user has successfully logged in
            flash(f'{user} has successfully logged in', 'success')
            # redirect to the home page
            return redirect(url_for('index'))
        else:
            flash('Username and/or password is incorrect', 'danger')
            
    return render_template('login.html', title=title, form=form)


@app.route('/logout')
def logout():
    logout_user()
    flash('You have successfully logged out', 'primary')
    return redirect(url_for('index'))


@app.route('/create-post', methods=['GET', 'POST'])
@login_required
def create_post():
    title = 'Create A Post'
    form = PostForm()
    if form.validate_on_submit():
        title = form.title.data
        body = form.body.data
        new_post = Post(title=title, body=body, user_id=current_user.id)
        flash(f"{new_post.title} has been created", 'secondary')
        return redirect(url_for('index'))
    return render_template('create_post.html', title=title, form=form)

@app.route('/my-posts')
@login_required
def my_posts():
    title = 'My Posts'
    posts = current_user.posts.all()
    return render_template('my_posts.html', title=title, posts=posts)

@app.route('/search-posts', methods=['GET', 'POST'])
def search_posts():
    title = 'Search'
    form = SearchForm()
    posts = []
    if form.validate_on_submit():
        term = form.search.data
        posts = Post.query.filter( (Post.title.ilike(f'%{term}%')) | (Post.body.ilike(f'%{term}%')) ).all()
    return render_template('search_posts.html', title=title, posts=posts, form=form)

@app.route('/posts/<post_id>')
@login_required
def single_post(post_id):
    post = Post.query.get_or_404(post_id)
    title = post.title
    return render_template('post_detail.html', title=title, post=post)

@app.route('/posts/<post_id>')
@login_required
def single_post(post_id):
    post = Post.query.get_or_404(post_id)
    title = post.title
    return render_template('post_detail.html', title=title, post=post)

# Edit a Single Post by ID
@app.route('/edit-posts/<post_id>', methods=["GET", "POST"])
@login_required
def edit_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        flash('You do not have edit access to this post.', 'danger')
        return redirect(url_for('my_posts'))
    title = f"Edit {post.title}"
    form = PostForm()
    if form.validate_on_submit():
        post.update(**form.data)
        flash(f'{post.title} has been updated', 'warning')
        return redirect(url_for('my_posts'))

    return render_template('post_edit.html', title=title, post=post, form=form)

@app.route('/delete-posts/<post_id>')
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        flash('You do not have delete access to this post', 'danger')
    else:
        post.delete()
        flash(f'{post.title} has been deleted.', 'secondary')
    return redirect(url_for('my_posts'))

@app.route('/view-addresses', methods=['GET', 'POST'])
def view_addresses():
    title = "All Addresses"
    addresses = Address.query.all()
    return render_template('view_addresses.html', title=title, addresses=addresses)

@app.route('/register-address', methods=['GET', 'POST'])
def register_address():
   title = "Register Address"
   form = AddressForm()
   addresses = Address.query.all()
   if form.validate_on_submit():
        first_name = form.first_name.data
        last_name = form.last_name.data
        name = first_name + last_name
        phone = form.phone_number.data
        address = form.address.data
        users_with_that_info = Address.query.filter(Address.phone_number==phone).all() 
        if users_with_that_info:
            flash(f"There is already a user with that phone-number. Please try again", "danger")
            return render_template('register_address.html', title=title, form=form)
        else:
            Address(first_name=first_name, last_name=last_name, address=address, phone_number=phone, user_id=current_user.id)
            return redirect(url_for('view_addresses'))

   return render_template('register_address.html', title=title, form=form, addresses=addresses)


@app.route('/my-addresses')
@login_required
def my_addresses():
   title = "My Addresses"
   addresses = current_user.addresses.all()
   return render_template('my_addresses.html', title=title, addresses=addresses)