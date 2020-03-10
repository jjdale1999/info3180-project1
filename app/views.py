"""
Flask Documentation:     http://flask.pocoo.org/docs/
Jinja2 Documentation:    http://jinja.pocoo.org/2/documentation/
Werkzeug Documentation:  http://werkzeug.pocoo.org/documentation/
This file creates your application.
"""
import os
from app import app, db
from flask import render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, current_user, login_required
from app.forms import CreateProfile
from app.models import UserProfile
from werkzeug.security import check_password_hash
from werkzeug.utils import secure_filename

###
# Routing for your application.
###

@app.route('/')
def home():
    """Render website's home page."""
    return render_template('home.html')


@app.route('/about/')
def about():
    """Render the website's about page."""
    return render_template('about.html')

@app.route('/profile',methods=['POST', 'GET'])
def profile():
    createprofile = CreateProfile()
    
    if request.method == "POST" and  createprofile.validate_on_submit():
                fname = createprofile.fname.data
                lname = createprofile.lname.data
                email = createprofile.email.data
                location= createprofile.location.data
                gender = createprofile.gender.data
                biography=createprofile.biography.data
                photo= createprofile.photo.data
                filename=secure_filename(photo.filename)
                photo.save(os.path.join(app.config['UPLOAD_FOLDER'],filename))
                user = UserProfile(fname, lname, email, location,gender,biography,'/uploads/'+filename)
                db.session.add(user)
                db.session.commit()

                return render_template("home.html")  # they should be redirected to a secure-page route instead
    else:
                flash_errors(createprofile)
    return render_template('addprofile.html',form=createprofile)    

@app.route('/profiles')
def profiles():
    user = UserProfile.query.all()
    print(user)


    # return render_template('users_show.html', id = num, users = users)
    return render_template('profiles.html',users=user)
    

@app.route('/profile/<userid>')
def profileuser(userid):
    """Render the website's about page."""  
    user = UserProfile.query.get(userid)
    fname = user.fname
    lname = user.lname
    email = user.email
    location= user.location
    gender = user.gender
    biography=user.biography
    photo= user.photo
    # return render_template('about.html', name="Mary Jane")
    return render_template('profile.html',lname=lname,email=email,location=location,gender=gender,biography=biography,photo=photo)


# Flash errors from the form if validation fails
def flash_errors(form):
    for field, errors in form.errors.items():
        for error in errors:
            flash(u"Error in the %s field - %s" % (
                getattr(form, field).label.text,
                error
            ), 'danger')

# ###
# The functions below should be applicable to all Flask apps.
###


@app.route('/<file_name>.txt')
def send_text_file(file_name):
    """Send your static text file."""
    file_dot_text = file_name + '.txt'
    return app.send_static_file(file_dot_text)


@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response


@app.errorhandler(404)
def page_not_found(error):
    """Custom 404 page."""
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port="8080")
