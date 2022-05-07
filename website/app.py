from flask import Flask
from website.extensions import db, migrate
from flask_login import LoginManager

def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config['SECRET_KEY'] = '10a9$*@&#3c;&%^#3453s'
    app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:wyBCu7Q1KyotPkxMbNGc@localhost/anotement"

    db.init_app(app)
    migrate.init_app(app, db)

    from website.routes import page_routes
    from website.routes.page_routes import page
    app.register_blueprint(page)

    from website.routes import note_routes
    from website.models.note import Note
    from website.routes.note_routes import note
    app.register_blueprint(note)

    from website.routes import todo_routes
    from website.models.todo import ToDo
    from website.routes.todo_routes import todo
    app.register_blueprint(todo)

    from website.routes import reminder_routes
    from website.models.reminder import Reminder
    from website.routes.reminder_routes import reminder
    app.register_blueprint(reminder)
    
    from website.routes import user_routes
    from website.models.user import User
    from website.routes.user_routes import user
    app.register_blueprint(user)

    from website.routes import video_routes
    from website.models.video import Video
    from website.routes.video_routes import video
    app.register_blueprint(video)

    login_manager = LoginManager()
    login_manager.login_view = "page.login"
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))
    
    return app
