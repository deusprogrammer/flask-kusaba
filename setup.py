import sys
import random
import re

from flask_kusaba.models import *
from elixir import *

if (len(sys.argv) != 2):
	print "You must enter a filename to create initial database"
	exit()

fname = sys.argv[1]
list = []
forum = None
section = None

try:
	f = open(fname)
except:
	print "File doesn't exist!"
	exit()

create_all()
setup_all()

for line in f.readlines():
	match = re.match(r"\s*(forum|section|board):([a-zA-Z0-9 ]+).*", line)
	if match:
		if match.group(1) == "forum":
			forum = Forum(
				name = match.group(2)
			)
			section = None
			print "CREATED FORUM %r" % forum
		elif match.group(1) == "section" and forum:
			section = Section(
				name = match.group(2),
				forum = forum
			)
			print "\tCREATED SECTION %r" % section
		elif match.group(1) == "board" and forum:
			match = re.match(r"\s*board:([a-zA-Z ]+)\s*\(([a-z]+)\)", line)
			if section:
				board = Board(
					name = match.group(1), 
					abbrev = match.group(2), 
					forum = forum,
					section = section
				)
			else:
				board = Board(
					name = match.group(1), 
					abbrev = match.group(2), 
					forum = forum
				)
			print "\t\tCREATED BOARD %r.%r.%r" % (forum, section, board)
			
	#match = re.match(r"\s*([a-zA-Z0-9]+):([a-zA-Z ]+)\s*\(([a-z]+)\)", line)
	#if match and forum:
	#	board = Board(name=match.group(1), abbrev=match.group(2), forum=forum)
	#	print "CREATED BOARD %r.%r" % (forum, board)
	#else:
	#	forum = Forum(name=line.replace("\n", ""))
	#	print "CREATED FORUM %r" % forum
			
session.commit()