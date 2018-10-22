from config import connex_app, collection
from flask_script import Manager, Shell, Server

manager = Manager(connex_app.app)

@manager.command
def runserver():
    connex_app.run(debug=True)

@manager.command
def test():
    