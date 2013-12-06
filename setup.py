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

try:
	f = open(fname)
except:
	print "File doesn't exist!"
	exit()

create_all()
setup_all()

for line in f.readlines():
	match = re.match(r"\s+([a-zA-Z ]+)\s*\(([a-z]+)\)", line)
	if match and forum:
		board = Board(name=match.group(1), abbrev=match.group(2), forum=forum)
		print "CREATED BOARD %r.%r" % (forum, board)
	else:
		forum = Forum(name=line.replace("\n", ""))
		print "CREATED FORUM %r" % forum
			
session.commit()