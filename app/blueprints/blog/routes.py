from . import blog
from flask import redirect, render_template, url_for, flash
from flask_login import login_required, current_user
from .forms import PostForm, SearchForm, AddressForm
from .models import Post, Address

@blog.route('/')
def index():
    title = 'Home'
    posts = Post.query.all()
    return render_template('index.html', title=title, posts=posts)


@blog.route('/create-post', methods=['GET', 'POST'])
@login_required
def create_post():
    title = 'Create A Post'
    form = PostForm()
    if form.validate_on_submit():
        title = form.title.data
        body = form.body.data
        new_post = Post(title=title, body=body, user_id=current_user.id)
        flash(f"{new_post.title} has been created", 'secondary')
        return redirect(url_for('blog.index'))
    return render_template('create_post.html', title=title, form=form)


@blog.route('/my-posts')
@login_required
def my_posts():
    title = 'My Posts'
    posts = current_user.posts.all()
    return render_template('my_posts.html', title=title, posts=posts)


# Get all posts that match search
@blog.route('/search-posts', methods=['GET', 'POST'])
def search_posts():
    title = 'Search'
    form = SearchForm()
    posts = []
    if form.validate_on_submit():
        term = form.search.data
        posts = Post.query.filter( (Post.title.ilike(f'%{term}%')) | (Post.body.ilike(f'%{term}%')) ).all()
    return render_template('search_posts.html', title=title, posts=posts, form=form)


# Get A Single Post by ID
@blog.route('/posts/<post_id>')
@login_required
def single_post(post_id):
    post = Post.query.get_or_404(post_id)
    title = post.title
    return render_template('post_detail.html', title=title, post=post)


# Edit a Single Post by ID
@blog.route('/edit-posts/<post_id>', methods=["GET", "POST"])
@login_required
def edit_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        flash('You do not have edit access to this post.', 'danger')
        return redirect(url_for('blog.my_posts'))
    title = f"Edit {post.title}"
    form = PostForm()
    if form.validate_on_submit():
        post.update(**form.data)
        flash(f'{post.title} has been updated', 'warning')
        return redirect(url_for('blog.my_posts'))

    return render_template('post_edit.html', title=title, post=post, form=form)


@blog.route('/delete-posts/<post_id>')
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        flash('You do not have delete access to this post', 'danger')
    else:
        post.delete()
        flash(f'{post.title} has been deleted.', 'secondary')
    return redirect(url_for('blog.my_posts'))


@blog.route('/register-address', methods=['GET', 'POST'])
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
            new_address = Address(first_name=first_name, last_name=last_name, address=address, phone_number=phone, user_id=current_user.id)
            flash(f"Address for {new_address.first_name} {new_address.last_name} has been created", "secondary")
            return redirect(url_for('blog.my_addresses'))

   return render_template('register_address.html', title=title, form=form, addresses=addresses)


@blog.route('/my-addresses')
@login_required
def my_addresses():
   title = "My Addresses"
   addresses = current_user.addresses.all()
   return render_template('my_addresses.html', title=title, addresses=addresses)
   

@blog.route('/view-addresses', methods=['GET', 'POST'])
def view_addresses():
    title = "All Addresses"
    addresses = Address.query.all()
    return render_template('address_detail.html', title=title, addresses=addresses)

# Edit a Single Route by ID
@blog.route('/edit-addresses/<address_id>', methods=["GET", "POST"])
@login_required
def edit_address(address_id):
    address = Address.query.get_or_404(address_id)
    if address.name != current_user:
        flash('You do not have edit access to this address.', 'danger')
        return redirect(url_for('blog.my_addresses'))
    title = f"Edit {address.first_name}"
    form = AddressForm()
    if form.validate_on_submit():
        address.update(**form.data)
        flash(f'Address for {address.first_name} {address.last_name} has been updated', 'warning')
        return redirect(url_for('blog.my_addresses'))

    return render_template('address_edit.html', title=title, address=address, form=form)


@blog.route('/delete-addresses/<address_id>')
@login_required
def delete_address(address_id):
    address = Address.query.get_or_404(address_id)
    if address.name != current_user:
        flash('You do not have delete access to this addreess', 'danger')
    else:
        flash(f'Address for {address.first_name} {address.last_name} has been deleted!')
        address.delete()
    return redirect(url_for('blog.my_addresses'))