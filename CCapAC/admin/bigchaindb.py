from flask import (
    Blueprint, 
    render_template, 
    request, 
    flash, 
    session, 
    redirect, 
    url_for)

from CCapAC.utils.token_verify import token_verify

from CCapAC.admin import bigchaindb_table
from tinydb import Query

bp = Blueprint("bigchainDB", __name__, url_prefix="/bigchainDB")

@bp.route("/index")
@token_verify
def index():
    assets = bigchaindb_table.search(Query().tx_type == "ASSET")
    services = bigchaindb_table.search(Query().tx_type == "SERVICE")
    profiles = bigchaindb_table.search(Query().tx_type == "PROFILE")
    statements = bigchaindb_table.search(Query().tx_type == "STATEMENT")

    data = {
        "assets" : assets,
        "services" : services,
        "profiles" : profiles,
        "statements" : statements,
    }
    return render_template('bigchaindb.html', title='Bigchain panel', data=data)