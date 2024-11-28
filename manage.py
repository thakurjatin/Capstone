import os
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from app import app, db

# Setup Migrate
migrate = Migrate(app, db)

# Setup Manager
manager = Manager(app)

# Add the 'db' commands to the manager
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
