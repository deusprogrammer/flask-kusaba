from elixir import *
import os
import datetime

metadata.bind = "sqlite:///bb.db"
metadata.bind.echo = True

class Forum(Entity):
	name     = Field(String(16))
	desc	 = Field(String(1024))
	sections = OneToMany('Section')
	boards   = OneToMany('Board')
	
	def __repr__(self):
		return self.name
		
class Section(Entity):
	name	= Field(String(16))
	forum	= ManyToOne('Forum')
	boards  = OneToMany('Board')
	
	def __repr__(self):
		return name
	
class Board(Entity):
	name    = Field(String(16))
	abbrev  = Field(String(4))
	threads = OneToMany('Thread', order_by='-updated')
	section = ManyToOne('Section')
	forum	= ManyToOne('Forum')
	
	def __repr__(self):
		return "%s(%s)" % (self.name, self.abbrev)
	
class Thread(Entity):
	subject = Field(String(16))
	created = Field(DateTime, default=datetime.datetime.now)
	updated = Field(DateTime, default=datetime.datetime.now)
	board   = ManyToOne('Board')
	posts   = OneToMany('Post')
	
	def __repr__(self):
		return "thread-%r" % self.id
	
class Post(Entity):
	subject 		= Field(String(16))
	text    		= Field(String(1024))
	created 		= Field(DateTime, default=datetime.datetime.now)
	poster_ip 		= Field(String(32))
	poster_email 	= Field(String(32))
	poster_name		= Field(String(32))
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