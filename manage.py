from commands.SeedRiak import SeedRiak
from commands.FlushRiak import FlushRiak
from flask import Flask
from flask.ext.script import Manager

app = Flask(__name__)
app.config.from_pyfile('config/default.cfg')

manager = Manager(app)
manager.add_command('riak:seed', SeedRiak())
manager.add_command('riak:flush', FlushRiak())

if __name__ == "__main__":
    manager.run()