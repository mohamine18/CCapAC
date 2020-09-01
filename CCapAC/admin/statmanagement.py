from flask import (
    Blueprint, 
    render_template, 
    request, 
    flash, 
    session, 
    redirect, 
    url_for)

from CCapAC.utils.token_verify import token_verify

import CCapAC.security.service as service
import CCapAC.security.profile as profile
import CCapAC.security.statement as statement


bp = Blueprint("statement", __name__, url_prefix="/statements")

@bp.route("/index")
@token_verify
def index():
    statement_instance = statement.Statement()
    statements = statement_instance.get_all()
    data = {
        "statements" : statements
    }
    return render_template('statements/statement.html', title='Statement management', data=data)

@bp.route("/create-statement", methods=['GET', 'POST'])
@token_verify
def create_statement():
    return render_template('statements/statementform.html', title='Create statement')