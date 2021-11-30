from flask import Flask, redirect, url_for
from flask_migrate import Migrate
from flask_login import LoginManager
from config import Config
from models import db


login_manager = LoginManager()


def create_app():
    _app = Flask(__name__)

    _app.config.from_object(Config())

    # init plugins
    db.init_app(_app)
    login_manager.init_app(_app)

    from views.home import home
    from views.auth import auth
    from views.artworks import artworks
    from views.gallery import gallery
    from api.likes import api_likes
    from api.images import api_images

    # register blueprints
    _app.register_blueprint(home, url_prefix='/')
    _app.register_blueprint(auth, url_prefix='/auth')
    _app.register_blueprint(artworks, url_prefix='/artworks')
    _app.register_blueprint(gallery, url_prefix='/gallery')
    _app.register_blueprint(api_likes, url_prefix='/api/likes')
    _app.register_blueprint(api_images, url_prefix='/api/images')

    migrate = Migrate(_app, db)

    from models.user import User

    @login_manager.user_loader
    def load_user(identifier):
        return User.query.get(int(identifier))

    # Error Management
    @_app.errorhandler(404)
    def page_not_found(error):
        return redirect(url_for('index.index'))

    db.create_all(app=_app)

    return _app


app = create_app()


if __name__ == '__main__':
    app.run(port=8000, debug=True)
