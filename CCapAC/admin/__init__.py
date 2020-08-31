from flask import Flask, redirect, url_for
from tinydb import TinyDB

#app
app = Flask(__name__)
app.config['SECRET_KEY'] = 'D494764E6F17137A9BA71EA56C742'

#TinyDB config
db = TinyDB('CCapAC/db.json')
asset_table = db.table('assets')

#index page redirect
@app.route("/")
def index():
    return redirect(url_for('tokenauth.login'))

#Bluprints registration
from CCapAC.admin import admin
from CCapAC.admin import tokenauth

app.register_blueprint(admin.bp)
app.register_blueprint(tokenauth.bp)