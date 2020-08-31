from flask import Blueprint
from flask import request, redirect, url_for, session, render_template, flash


bp = Blueprint("tokenauth", __name__, url_prefix="/auth")

@bp.route("/login", methods=['GET','POST'])
def login():
    if request.method == 'POST':
        if request.form['token'] == "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6Im1vaGFtaW5lMTgiLCJwYXNzd29yZCI6IjE5OTEifQ.Q6JDqfYHVwzRYzGFLiFmfmFaD5cU3mEYjIx8Ft-XPic" :
            session['username'] = request.form['token']
            return redirect(url_for('admin.index'))
        else:
            flash("Token Invalid", 'danger')
    return render_template('login.html', title='Login')

@bp.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('tokenauth.login'))
    
        
    
