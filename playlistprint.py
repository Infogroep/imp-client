import sys
import os
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/clint")
from clint.textui import colored
from impversion import IMP_VERSION
from animp import an_imp
from datetime import timedelta

def same(x):
	return x

class Column:
	def __init__(self,size,justification = "left"):
		self.size = size
		self.justification = justification

class Content:
	def __init__(self,text,contype = "std",coloring = same):
		self.coloring = coloring
		self.text = text
		self.type = contype

class TableWriter:
	def __init__(self,cols):
		self.cols = cols

	def format_cols(self,contents):
		filler = contents[-1] if len(contents) > len(self.cols) else " "

		def adjust_data_size(content,colsize):
			if len(content.text) <= colsize:
				return content.text
			elif content.type == "uri":
				return "..." + content.text[-(colsize - 3):]
			else:
				return content.text[:(colsize - 3)] + "..."

		def col_size():
			return desired + (len(str(con)) - len(con))

		def justify(col,content):
			if col.justification == "right":
				return content.rjust(col.size, filler)
			elif col.justification == "center":
				return content.center(col.size, filler)
			else:
				return content.ljust(col.size, filler)

		def format_column((col,content)):
			return filler + content.coloring(justify(col,adjust_data_size(content, col.size))) + filler

		return "|%s|" % "|".join(map(format_column, zip(self.cols,contents)))
	
	def printBorder(self):
		print(self.format_cols(map(Content,[""] * len(self.cols)) + ["*"]))

	def printHeader(self,*args):
		print(self.format_cols(map(lambda text: Content(text, "std", colored.bright), args)))

	def printBody(self,*args):
		print(self.format_cols(args))

	

def printPlaylist(pl):
	t = TableWriter([Column(37,"center"),Column(3,"right"),Column(30),Column(18),Column(8,"right"),Column(8)])
	t.printBorder()
	t.printHeader("imp version " + IMP_VERSION, "No.", "Title", "Artist", "Duration", "Queuedby")
	t.printBorder()
	i = 0	
	for media in pl:
		t.printBody(
			Content(an_imp[i], "std", colored.green) if i < len(an_imp) else Content(""),
			Content(str(i)) if i > 0 else Content("> 0"),
			Content(media["info"]["title"]) if "title" in media["info"] else Content(media["uri"],"uri") if media["uri"].find("tmp/cache/") != 0 else Content("Unknown"),
			Content(media["info"]["artist"]) if "artist" in media["info"] else Content("Unknown"),
			Content(str(timedelta(seconds=round(float(media["info"]["duration"]))))) if "duration" in media["info"] else Content("Forever"),
			Content(media["info"]["user"]) if "user" in media["info"] else Content("John Doe"))
		i += 1

	if i < len(an_imp):
		for j in range(i,len(an_imp)):
			t.printBody(Content(an_imp[j], "std", colored.green),Content(""),Content(""),Content(""),Content(""),Content(""))
	t.printBorder()

