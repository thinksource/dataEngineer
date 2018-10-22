from config import connex_app, collection
from flask_script import Manager, Shell

manager = Manager(connex_app.app)
def _make_context():
    """Return context dict for a shell session so you can access
    app, db, and the User model by default.
    """
    return {'app': connex_app, 'collection': collection}

@manager.command
def runserver():
    connex_app.run(debug=True)

@manager.command
def test():
    import pytest
    exit_code = pytest.main(['test_server.py','-v'])
    return exit_code


manager.add_command('shell', Shell(make_context=_make_context))

if __name__ == '__main__':
    manager.run()