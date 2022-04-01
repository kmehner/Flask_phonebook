from app import app, db
from app.blueprints.auth.models import User
from app.blueprints.blog.models import Post

@app.shell_context_processor
def make_context():
    return {'db': db, 'User': User, 'Post': Post}