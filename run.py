
from app import app, db 
from app.models import Post, User, Submit

@app.shell_context_processor
def make_shell_contextP():
    return {
        'db': db,
        'Post': Post,
        'User': User,
        'Submit': Submit
    }