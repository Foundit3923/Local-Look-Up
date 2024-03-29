Cloudinary Django Project
================================

A simple web application that uses AI to identify photos/images and then searchs for related local businesses and locations, returning google maps directions.
The web app allows you to upload photos, maintain a database with references to them, list them with their metadata, and display them using various cloud-based transformations.

*NOTE:* THIS PROJECT IS OUT OF DATE, DO NOT EXPECT FULL FUNCTIONALITY

This project depends on [Cloudinary's Python library](https://github.com/cloudinary/pycloudinary). 

## Installation

Run the following commands from your shell.

Project cloning and dependent package installation: 

    git clone git://github.com/cloudinary/cloudinary-django.git    
    cd cloudinary-django
    pip install -r requirements.txt

Defining Cloudinary's credentials. The CLOUDINARY_URL value is available in the [dashboard of your Cloudinary account](https://cloudinary.com/console). 
If you don't have a Cloudinary account yet, [click here](https://cloudinary.com/users/register/free) to create your free account.
     
    export CLOUDINARY_URL=cloudinary://<API-KEY>:<API-SECRET>@<CLOUD-NAME>
    
Creating a local database and running a web server:
      
    python ./manage.py migrate --run-syncdb
    python ./manage.py runserver

You can now browse to the [following link](http://localhost:8000/) to start exploring the project.

	http://localhost:8000/
	    
The app also supports the Django admin which is available [here](http://localhost:8000/admin):

	http://localhost:8000/admin

### With virtualenv

We recommend and support the usage of **virtualenv**. All you need to do is create a new virtualenv (if necessary):

    virtualenv venv

And then just activate it:

    source venv/bin/activate

Now you can go ahead with the instructions above.
