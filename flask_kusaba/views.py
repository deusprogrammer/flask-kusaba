from flask import *
from model import *
from flask_kusaba import app

@app.route('/forum/<forum_id>/')
def show_boards(forum_id):
	forum = Forum.query.filter_by(name=forum_id).one()
	for board in forum.boards:
		print board
	
	return render_template('boards.html', forum=forum)

@app.route('/forum/<forum_id>/board/<board_id>')
@app.route('/forum/<forum_id>/board/<board_id>/page/<page>')
def show_board(forum_id, board_id, page=1):
	forum = Forum.query.filter_by(name=forum_id).one()
	board = Board.query.filter_by(abbrev=board_id, forum=forum).one()
	for thread in board.threads:
		print thread
	return render_template('board.html', board=board)
	
@app.route('/forum/<forum_id>/board/<board_id>/thread/<thread_id>')
def show_thread(forum_id, board_id, thread_id):
	forum  = Forum.query.filter_by(name=forum_id).one()
	board  = Board.query.filter_by(abbrev=board_id, forum=forum).one()
	thread = Thread.query.filter_by(id=thread_id, board=board).one()
	for post in thread.posts:
		print post
	return render_template('thread.html', thread=thread)
	
if __name__ == "__main__":
    app.run()
