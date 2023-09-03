
from helpmate.index import create_app

import os
import configparser


config = configparser.ConfigParser()
config.read(os.path.abspath(os.path.join(".ini")))

if __name__ == "__main__":
    app = create_app()
    app.config['DEBUG'] = True
    app.config['JWT_SECRET_KEY'] = config['TEST']['JWT_SECRET_KEY']
    app.config['MONGO_URI'] = config['TEST']['DB_URI']

    app.run()
