from elixir import *
import os

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
	has_one('image', of_kind='Image', inverse='post')
	thread  = ManyToOne('Thread')
	
	def __repr__(self):
		return "post-%r" % self.id
		
class Image(Entity):
	filename = Field(String(32))
	thumbnail = Field(String(32))
	belongs_to('post', of_kind='Post')
	
	def __repr__(self):
		return "image-%r" % self.id
	
	def getBytes(self):
		file = open(self.filename, "rb")
		return file.read()
		
	def getThumbBytes(self):
		file = open(self.thumbnail, "rb")
		return file.read()