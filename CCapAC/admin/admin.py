from flask import (
    Blueprint, 
    render_template, 
    request, 
    flash, 
    session, 
    redirect, 
    url_for)

from CCapAC.utils.token_verify import token_verify

import CCapAC.security.asset as asset
import CCapAC.security.service as service
import CCapAC.security.profile as profile

bp = Blueprint("admin", __name__, url_prefix="/admin")

@bp.route("/index")
@token_verify
def index():
    assets_instance = asset.Asset()
    assets = assets_instance.get_all()

    service_instance = service.Service()
    services = service_instance.get_all()

    profile_instance = profile.Profile()
    profiles = profile_instance.get_all()

    data = {
        "assets" : assets,
        "services" : services,
        "profiles" : profiles
    }
    return render_template('admin.html', title='Admin panel', data=data)

@bp.route("/add-asset", methods=['GET','POST'])
@token_verify
def add_asset():
    if request.method == 'POST':
        if not request.form['entity_id'] or not request.form['entity_uri_domain'] or not request.form['entity_uri_location'] or not request.form['entity_uri_resource']:
            flash("Please fill all the form", 'danger')
        else:
            entity_uri = f"{request.form['entity_uri_domain']}:{request.form['entity_uri_location']}:{request.form['entity_uri_resource']}"
            assets_instance = asset.Asset(entity_owner=request.form['entity_org'],entity_id=request.form['entity_id'], entity_type=request.form['entity_type'], asset_issuer=session['username'], entity_uri=entity_uri, entity_func=request.form['entity_func'])
            insert = assets_instance.create_asset()
            if not insert:
                flash('Insertion error', 'danger')
            elif insert == True:
                 flash('Asset already exist', 'warning')
            else:
                flash('Assset added successfully', 'success')
                return redirect(url_for('admin.index'))
    return render_template('assetform.html', title='Add Asset')

@bp.route("/add-service", methods=['GET','POST'])
@token_verify
def add_service():
    if request.method == 'POST':
        if not request.form['service_name'] or not request.form['service_init'] or not request.form['sm_number'] or not request.form['req_quota']:
            flash("Please fill all the form", 'danger')
        else:
            service_instance = service.Service(service_name=request.form['service_name'], service_init=request.form['service_init'], service_issuer=session['username'], sm_number=request.form['sm_number'], req_quota=request.form['req_quota'])
            insert = service_instance.create_service()
            if not insert:
                flash('Insertion error', 'danger')
            elif insert == True:
                flash('Service already exist', 'warning')
            else:
                flash('Service added successfully', 'success')
                return redirect(url_for('admin.index'))
    return render_template('serviceform.html', title='Add Service')


@bp.route("/create-profile", methods=['GET', 'POST'])
@token_verify
def create_profile():
    if request.method == 'POST':
        if not request.form['asset_id'] or not request.form['service_id']:
            flash('Please fill all the form', 'danger')
        else:
            profile_instance = profile.Profile(asset_id=request.form['asset_id'], service_id=request.form['service_id'], profile_issuer=session['username'])
            insert = profile_instance.create_profile()
            if not insert:
                flash('Insertion error', 'danger')
            elif insert == True:
                flash('profile already exist', 'warning')
            else:
                flash('Profile Created successfully', 'success')
                return redirect(url_for('admin.index'))    

    assets_instance = asset.Asset()
    assets = assets_instance.get_all()

    service_instance = service.Service()
    services = service_instance.get_all()

    data = {
        "assets" : assets,
        "services" : services,
    }
    return render_template('profileform.html', title='Create profile', data=data)

@bp.route("create-statement", methods=['GET', 'POST'])
@token_verify
def create_statement():
    return render_template('statementform.html', title='Create statement')