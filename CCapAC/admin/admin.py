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

bp = Blueprint("admin", __name__, url_prefix="/admin")

@bp.route("/index")
@token_verify
def index():
    assets_instance = asset.Asset()
    assets = assets_instance.get_all()
    return render_template('admin.html', title='Admin panel', assets=assets)

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


