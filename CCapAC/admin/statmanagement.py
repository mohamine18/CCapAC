from flask import (
    Blueprint, 
    render_template, 
    request, 
    flash, 
    session, 
    redirect, 
    url_for,
    jsonify)

from CCapAC.utils.token_verify import token_verify
import jwt 
import json
from tinydb import Query
import datetime

import CCapAC.security.service as service
import CCapAC.security.profile as profile
import CCapAC.security.statement as statement

from CCapAC.admin import tokens_table, profile_table, service_table, asset_table


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

@bp.route("/tokens", methods=['GET','POST'])
@token_verify
def tokens():
    decode = False
    # Authentication
    if request.method == 'POST':
        t1 = datetime.datetime.now()
        if not request.form['token']:
            flash('Please provide a token', 'warning')
            return redirect(url_for('statement.tokens'))
        token = bytes(request.form['token'], 'utf-8')
        # Signature verification
        try:
            decode = jwt.decode(token, 'secret', algorithms='HS256')
        except:
            flash('Signature verification failed', 'danger')
            return redirect(url_for('statement.tokens'))
        # Profile verification
        profile_id =  decode["statementCredential"]["profile_id"]
        profile_exist = profile_table.search(Query().context.id == profile_id)
        text = dict(profile_exist[0])
        if not profile_exist:
            flash("Profile don't exist", "danger")
            return redirect(url_for('statement.tokens'))
        
        # Service and asset verification
        service_id = text["profileCredential"]["service_id"]
        service_exist = service_table.search(Query().context.id == service_id)
        if not service_exist:
            flash("Service don't exist", "danger")
            return redirect(url_for('statement.tokens'))

        # Asset verification
        asset_id = text["profileCredential"]["asset_id"]
        asset_exist = asset_table.search(Query().context.uid == asset_id)
        if not asset_exist:
            flash("Asset don't exist", "danger")
            return redirect(url_for('statement.tokens'))
        
        t2 = datetime.datetime.now()
        
        
        print(f"Time start: {t1.strftime('%S.%f')}, Time end: {t2.strftime('%S.%f')}")



    tokens = tokens_table.all()
    data = {
        "tokens" : tokens,
        "decode" : decode
    }
    return render_template('statements/tokens.html', title='Tokens management', data=data)

@bp.route("/create-statement", methods=['GET', 'POST'])
@token_verify
def create_statement():
    if request.method == 'POST':
        if not request.form['service_id'] or not request.form['profile_id'] or not request.form['action']:
            flash("Please fill all the form", 'danger')
        else:
            statement_instance = statement.Statement(st_issuer=session['username'], st_action=request.form['action'], st_profile_id=request.form['profile_id'])
            insert = statement_instance.create_statement()
            if not insert:
                flash('Insertion error', 'danger')
            elif insert == True:
                 flash('Asset already exist', 'warning')
            else:
                flash('Assset added successfully', 'success')
                return redirect(url_for('statement.index'))
                
    service_instance = service.Service()
    services = service_instance.get_all()
    if not services:
        flash('Please add services first', 'warning')
    data = {
        "services" : services,
    }
    return render_template('statements/statementform.html', title='Create statement', data=data)

#API
@bp.route("/api/v1/services/profiles", methods=['GET'])
def get_service_profiles():
    """
    returns a list of profiles (assets) related to a service
    used in statement creation form
    param: service_id
    """
    if 'service_id' in request.args:
        profile_instance = profile.Profile()
        profiles = profile_instance.service_assets_profiles(request.args['service_id'])
        return jsonify(profiles)
    else:
        return jsonify('please provide a service identifier'), 403