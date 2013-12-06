flask-kusaba
============
Flask Kusaba is a 4chan (Kusaba) like message board.  It is designed using the Flask microframework and the Elixir ORM.  This web app only runs under Python 2.6 or higher, but not Python 3.

Before launching, you must run the setup.py script.  You must pass in a file of the following format:

forum1
	board1(board_abbrev1)
	board2(board_abbrev2)
	...
forum2
	board1(board_abbrev1)
	board2(board_abbrev2)
	...
...

With this file you run the setup.py script as follows:

setup.py forum_data_filename