"""
Flask Documentation:     https://flask.palletsprojects.com/
Jinja2 Documentation:    https://jinja.palletsprojects.com/
Werkzeug Documentation:  https://werkzeug.palletsprojects.com/
This file contains the routes for your application.
"""
import os
from app import app, db
from flask import render_template, request, redirect, url_for, flash, send_from_directory
from werkzeug.utils import secure_filename
from app.forms import PropertyForm
from app.models import Property


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
    return render_template('about.html', name="Mary Jane")



@app.route('/properties/create', methods=['GET', 'POST'])
def create_property():
    form = PropertyForm()
    if form.validate_on_submit():
        title = form.title.data
        description = form.description.data
        noOfRooms = form.noOfRooms.data
        noOfBathrooms = form.noOfBathrooms.data
        price = form.price.data
        propertyType = form.propertyType.data
        location = form.location.data
        photo = form.photo.data
        filename = secure_filename(photo.filename)
        photo.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        
        # store the form data in a database
        db.session.add(Property(title, description, noOfRooms, noOfBathrooms, price, propertyType, location, filename))
        db.session.commit()
        
        flash('Property successfully added', 'success')
        return redirect(url_for('properties'))
    
    flash_errors(form)
    return render_template('create_property.html', form=form)

@app.route('/properties')
def properties():
    properties = Property.query.all()
    # fetch the photo for each property from the uploads folder
    # check that the photo name from the database is in the uploads folder using the get_uploaded_images function
    images = get_uploaded_images()
    for property in properties:
        if property.photo in images:
            property.photo = url_for('uploaded_file', filename=property.photo)
    return render_template('properties.html', properties=properties) 


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(os.path.join(os.getcwd(), app.config['UPLOAD_FOLDER']), filename)

@app.route('/properties/<int:propertyid>')
def property(propertyid):
    property = Property.query.filter_by(id=propertyid).first()
    property.photo = url_for('uploaded_file', filename=property.photo)
    return render_template('property.html', property=property)


def get_uploaded_images():
    rootdir = os.getcwd()
    # print(rootdir)
    image_list = []
    for subdir, dirs, files in os.walk(os.path.join(rootdir, app.config['UPLOAD_FOLDER'])):
        for file in files:
            # print(os.path.join(subdir, file))
            if file.endswith(('.jpg', '.png', '.jpeg')):
                full_path = os.path.join(subdir, file)
                relative_path = os.path.relpath(full_path, os.path.join(rootdir, app.config['UPLOAD_FOLDER']))
                image_list.append(relative_path)
    return image_list




###
# The functions below should be applicable to all Flask apps.
###

# Display Flask WTF errors as Flash messages
def flash_errors(form):
    for field, errors in form.errors.items():
        for error in errors:
            flash(u"Error in the %s field - %s" % (
                getattr(form, field).label.text,
                error
            ), 'danger')

@app.route('/<file_name>.txt')
def send_text_file(file_name):
    """Send your static text file."""
    file_dot_text = file_name + '.txt'
    return app.send_static_file(file_dot_text)


@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also tell the browser not to cache the rendered page. If we wanted
    to we could change max-age to 600 seconds which would be 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response


@app.errorhandler(404)
def page_not_found(error):
    """Custom 404 page."""
    return render_template('404.html'), 404
