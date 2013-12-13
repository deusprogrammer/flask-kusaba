from flask import *
from flask_login import login_user, logout_user, login_required, current_user

from models import *
from auth import *
from flask_kusaba import app

import os
import imghdr
import time
import math
import datetime
import Image as _Image

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
THREADS_PER_PAGE = 10.0
POSTS_PER_PREVIEW = 4

@app.before_request
def before_request():
	print "IN FILTER WITH PATH %s" % request.path
	print "CURRENT USER %s" % current_user.get_username()
	print "ANONYMOUS? %r" % current_user.is_anonymous()
	banned = Banned.query.filter_by(poster_ip=request.remote_addr)
	if banned.count() > 0 and not request.path == '/banned' :
		banned = banned.one()
		return redirect(url_for('banned', reason=banned.reason))
	return

@app.route('/banned')	
def banned():
	banned = Banned.query.filter_by(poster_ip=request.remote_addr).one()
	return "You are banned.<br />Reason: \"%s\"" % banned.reason
	
@app.route('/user/ban/ip/<poster_ip>')
@login_required
def ban_user(poster_ip):
	Banned(
		poster_ip = poster_ip,
		reason = "User posted some stupid shit!"
	)
	session.commit()
	return "User banned on ip %s" % poster_ip

@app.route('/user/login/')
def login():
	return render_template(
		'login.html'
	)

@app.route('/user/auth/', methods=['POST'])
def authenticate():
	username = request.form['username']
	password = request.form['password']
	
	user = authenticate_user(username, password)
	
	if user and user.is_authenticated():
		login_user(user)
	else:
		return redirect(url_for('login'))
		
	return redirect(url_for('show_boards', forum_id='ponychan'))
	
@app.route('/user/logout/')
def logout():
	logout_user()
	return redirect(url_for('show_boards', forum_id='ponychan'))
	
@app.route('/forum/<forum_id>/')
def show_boards(forum_id):
	forum = Forum.query.filter_by(name=forum_id).one()
	return render_template(
		'boards.html', 
		forum = forum
	)

@app.route('/forum/<forum_id>/board/<board_id>')
@app.route('/forum/<forum_id>/board/<board_id>/page/<page>')
def show_board(forum_id, board_id, page=1):
	forum = Forum.query.filter_by(name=forum_id).one()
	board = Board.query.filter_by(abbrev=board_id, forum=forum).one()
	
	page = int(page)
	n_pages = int(math.ceil(len(board.threads)/THREADS_PER_PAGE))
	start_thread = int(math.floor((page - 1) * THREADS_PER_PAGE))
	end_thread = int(math.floor(((page - 1) * THREADS_PER_PAGE) + THREADS_PER_PAGE))
	
	return render_template(
		'board.html', 
		board = board, 
		page = page, 
		n_pages = n_pages, 
		start_thread = start_thread, 
		end_thread = end_thread, 
		posts_per_preview = POSTS_PER_PREVIEW, 
		admin = current_user.is_admin()
	)
	
@app.route('/forum/<forum_id>/board/<board_id>/thread/<thread_id>')
def show_thread(forum_id, board_id, thread_id):
	forum  = Forum.query.filter_by(name=forum_id).one()
	board  = Board.query.filter_by(abbrev=board_id, forum=forum).one()
	thread = Thread.query.filter_by(id=thread_id, board=board).one()
	return render_template(
		'thread.html', 
		thread = thread, 
		posts_per_preview = POSTS_PER_PREVIEW,
		admin = current_user.is_admin()
	)
	
@app.route('/forum/<forum_id>/board/<board_id>/post', methods=['POST'])
@app.route('/forum/<forum_id>/board/<board_id>/thread/<thread_id>/post', methods=['POST'])
def create_post(forum_id, board_id, thread_id=-1):
	if request.method == 'POST':
		forum  = Forum.query.filter_by(name=forum_id).one()
		board  = Board.query.filter_by(abbrev=board_id, forum=forum).one()
		if (thread_id != -1):
			thread = Thread.query.filter_by(id=thread_id, board=board).one()
			thread.updated = datetime.datetime.now()
		else:
			thread = Thread(
				subject = request.form['subject'], 
				board = board
			)

		name = request.form['name']
		
		if not request.form['name']:
			name = 'Anonymous'
			
		post = Post(
			subject = request.form['subject'], 
			text = request.form['text'], 
			poster_email = request.form['email'], 
			poster_name = name,
			poster_ip = request.remote_addr, 
			thread = thread
		)
	
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
	
	return redirect(
		url_for('show_thread', 
		forum_id = forum_id, 
		board_id = board_id, 
		thread_id = thread.id)
	)
		
	
@app.route('/image/<image_id>')
def get_image(image_id):
	image = Image.query.filter_by(id=image_id).one()
	bytes = image.getBytes()
	mimetype = 'image/%s' % imghdr.what(image.filename)
	return Response(
		bytes, 
		mimetype = mimetype
	)

@app.route('/image/<image_id>/thumbnail')
def get_thumbnail(image_id):
	image = Image.query.filter_by(id=image_id).one()
	bytes = image.getThumbBytes()
	mimetype = 'image/%s' % imghdr.what(image.filename)
	return Response(
		bytes, 
		mimetype = mimetype
	)