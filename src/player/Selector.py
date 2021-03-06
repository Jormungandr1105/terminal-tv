################################################################################
##  Terminal_TV Selector                                                      ##
####  author: jormungandr                                                   ####
####  exec: none                                                            ####
####  created: 01/13/22                                                     ####
################################################################################
# Imports from src
from src.io.Directory import Directory
from src.io.Episode import Episode
from src.io.FileReader import FileReader
import src.player.Screens as Screens
# Library Imports
import math
import os

class Selector:

	def __init__(self, media_path):
		self.cursor = 0
		self.backup_cursor = 0
		# TARGETS:
		# 0 -> Main_Tree
		# 1 -> Recovery
		self.target = 0
		self.media_dir = Directory(media_path,"",True)
		self.recovery_time = None

	# Cursor Manipulation
	def increment_main_cursor(self):
		if self.cursor < len(self.files[0])-1:
			self.cursor+=1

	def decrement_main_cursor(self):
		if self.cursor > 0:
			self.cursor-=1

	def increment_backup_cursor(self,length):
		self.backup_cursor = min(self.backup_cursor+1,length-1)

	def decrement_backup_cursor(self):
		self.backup_cursor = max(self.backup_cursor-1,0)

	# Dealing with Directories and Files
	def update_files(self):
		self.files = self.media_dir.folder_array("")

	def toggle(self,player):
		file = self.get_filedata()
		if self.target == 0:
			#file = self.get_filedata()
			if isinstance(file,Directory):
				# Change the visibility of the directory
				file.toggle_visibility()
				self.update_files()
			else:
				# Queue the video
				episode = Episode(file)
				episode.read_episode()
				if episode.time <= 30:
					player.queue(episode)
				else:
					self.target = 1
					self.episode = episode
		elif self.target == 1:
			self.target = 0
			if self.backup_cursor == 0:
				player.queue(self.episode)
			else:
				self.episode.time = 0
				player.queue(self.episode)

	# GETTERS
	def get_filename(self):
		return self.files[0][self.cursor]

	def get_filedata(self):
		return self.files[1][self.cursor]