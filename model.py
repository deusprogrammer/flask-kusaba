from elixir import *

metadata.bind = "sqlite:///bb.db"
metadata.bind.echo = True

class Forum(Entity):
	name    = Field(String(16))
	desc	= Field(String(1024))
	boards  = OneToMany('Board')
	
	def __repr__(self):
		return self.name
	
class Board(Entity):
	name    = Field(String(16))
	abbrev  = Field(String(4))
	threads = OneToMany('Thread')
	forum   = ManyToOne('Forum')
	
	def __repr__(self):
		return "%s(%s)" % (self.name, self.abbrev)
	
class Thread(Entity):
	subject = Field(String(16))
	board   = ManyToOne('Board')
	posts   = OneToMany('Post')
	
	def __repr__(self):
		return "thread-%r" % self.id
	
class Post(Entity):
	subject = Field(String(16))
	text    = Field(String(1024))
	thread  = ManyToOne('Thread')
	
	def __repr__(self):
		return "post-%r" % self.id