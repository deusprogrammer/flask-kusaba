flask-kusaba
============

This is a web application that mirrors the functionality of message boards like 4chan, except it's written with the lightweight Python framework, flask.

This version boasts some improvements however, such as jQuery elements that show the image preview in a modal and each page will display a spinner modal until all images are loaded.

Before running the script you must install the flask and elixir modules.  This is easily done with easy_install or pip.

In order to use this application...first you must run the setup.py script.  To use the script you must pass in a template file with a format similiar to the following:

    forum
      board(abbrev)
      board(abbrev)
      board(abbrev)
    forum
      board(abbrev)
      board(abbrev)
      
After running setup.py, you just run runserver.py
