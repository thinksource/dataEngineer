import os
import connexion
import pymongo
import json
basedir = os.path.abspath(os.path.dirname(__file__))

# Create the connexion application instance
connex_app = connexion.FlaskApp(__name__, specification_dir=basedir)

# print(basedir)
# Get the underlying Flask app instance
app = connex_app.app


# Build the Sqlite ULR for SqlAlchemy
# sqlite_url = 'sqlite:////' + os.path.join(basedir, 'people.db')
file=open('..\\db.txt','r')

# Configure the SqlAlchemy part of the app instance

app.config['DATABASE_URI'] = file.read()  

client = pymongo.MongoClient(app.config['DATABASE_URI'])
collection=json.load(open("..\\testdb.json"))
collection = client['crawlerdb']['news']
# app.collection=collection
connex_app.add_api('swagger.yml')