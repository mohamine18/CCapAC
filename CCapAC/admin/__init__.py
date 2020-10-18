from flask import Flask, redirect, url_for
from tinydb import TinyDB

#app
app = Flask(__name__)
app.config['SECRET_KEY'] = 'D494764E6F17137A9BA71EA56C742'

#TinyDB config
db = TinyDB('CCapAC/db.json')
asset_table = db.table('assets')
service_table = db.table('services')
profile_table = db.table('profiles')
statement_table = db.table('statements')
bigchaindb_table = db.table('bigchaindb')
tokens_table = db.table('tokens')

#index page redirect
@app.route("/")
def index():
    return redirect(url_for('tokenauth.login'))

#Bluprints registration
from CCapAC.admin import admin
from CCapAC.admin import tokenauth
from CCapAC.admin import statmanagement
from CCapAC.admin import bigchaindb

app.register_blueprint(admin.bp)
app.register_blueprint(tokenauth.bp)
app.register_blueprint(statmanagement.bp)
app.register_blueprint(bigchaindb.bp)