from flask import Flask
from models import *
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://jokin:12345@192.168.1.75:5432/dbprueba'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db.init_app(app)
migrate = Migrate(app, db)
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run()
