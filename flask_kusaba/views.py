from flask import *

from models import *
from flask_kusaba import app

import os
import imghdr
import time
import math
import Image as _Image

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

setup_all()

def allowed_file(filename):
    return imghdr.what(image.filename) in ALLOWED_EXTENSIONS

@app.route('/forum/<forum_id>/')
def show_boards(forum_id):
	forum = Forum.query.filter_by(name=forum_id).one()
	return render_template('boards.html', forum=forum)

@app.route('/forum/<forum_id>/board/<board_id>')
@app.route('/forum/<forum_id>/board/<board_id>/page/<page>')
def show_board(forum_id, board_id, page=1):
	forum = Forum.query.filter_by(name=forum_id).one()
	board = Board.query.filter_by(abbrev=board_id, forum=forum).one()
	return render_template('board.html', board=board)
	
@app.route('/forum/<forum_id>/board/<board_id>/thread/<thread_id>')
def show_thread(forum_id, board_id, thread_id):
	forum  = Forum.query.filter_by(name=forum_id).one()
	board  = Board.query.filter_by(abbrev=board_id, forum=forum).one()
	thread = Thread.query.filter_by(id=thread_id, board=board).one()
	return render_template('thread.html', thread=thread)
	
@app.route('/forum/<forum_id>/board/<board_id>/post', methods=['POST'])
@app.route('/forum/<forum_id>/board/<board_id>/thread/<thread_id>/post', methods=['POST'])
def create_post(forum_id, board_id, thread_id=-1):
	if request.method == 'POST':
		forum  = Forum.query.filter_by(name=forum_id).one()
		board  = Board.query.filter_by(abbrev=board_id, forum=forum).one()
		if (thread_id != -1):
			thread = Thread.query.filter_by(id=thread_id, board=board).one()
		else:
			thread = Thread(subject=request.form['subject'], board=board)

		post = Post(subject=request.form['subject'], text=request.form['text'], thread=thread)
	
		file = request.files['file']
		if file:
			size = 200, 200
			filename = "%d" % math.floor(time.time())
			fullsize_file = os.path.join(app.config['UPLOAD_FOLDER'], filename)
			thumbnail_file = os.path.join(app.config['UPLOAD_FOLDER'], "%s_thumbnail.png" % filename)
			
			file.save(fullsize_file)
			
			image = _Image.open(fullsize_file)
			image.thumbnail(size)
			image.save(thumbnail_file)
			Image(filename=fullsize_file, thumbnail=thumbnail_file, post=post)
			
		session.commit()
	
	return redirect(url_for('show_thread', forum_id=forum_id, board_id=board_id, thread_id=thread.id))
		
	
@app.route('/image/<image_id>')
def get_image(image_id):
	image = Image.query.filter_by(id=image_id).one()
	bytes = image.getBytes()
	mimetype = 'image/%s' % imghdr.what(image.filename)
	return Response(bytes, mimetype=mimetype)

@app.route('/image/<image_id>/thumbnail')
def get_thumbnail(image_id):
	image = Image.query.filter_by(id=image_id).one()
	bytes = image.getThumbBytes()
	mimetype = 'image/%s' % imghdr.what(image.filename)
	return Response(bytes, mimetype=mimetype)