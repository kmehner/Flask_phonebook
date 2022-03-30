from app import app
from flask import redirect, render_template, url_for
from app.forms import AddressForm, SignUpForm
from app.models import User, Address, Post

@app.route('/')
def index():
   title = "Home"
   return render_template('index.html', title=title)

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
        # Create a new user instance with form data
        new_user = User(email=email, username=username, password=password)
        return redirect(url_for('index'))

    return render_template('signup.html', title=title, form=form)


@app.route('/login')
def login():
    title = 'Log In'
    return render_template('login.html', title=title)

@app.route('/register_phone_number', methods=['GET', 'POST'])
def register_phone_number():
   title = "Register Phone Number"
   form = AddressForm()
   addresses = Address.query.all()
   if form.validate_on_submit():
      first_name = form.first_name.data
      last_name = form.last_name.data
      phone = form.phone_number.data
      address = form.address.data
      Address(first_name=first_name, last_name=last_name, address=address, phone_number=phone)
      return redirect(url_for('index'))


   return render_template('register_address.html', title=title, form=form)