#!/usr/bin/env python
import sys
import gtk
import appindicator

import gobject
import sqlite3

# http://developer.ubuntu.com/api/ubuntu-11.10/python/AppIndicator-0.1.html

sqlite_db = "/home/bart/.thunderbird/ug524fiy.default/global-messages-db.sqlite"

class Thunderbird:
	def __init__(self):
		self.ind = appindicator.Indicator("new-mail-indicator", "", appindicator.CATEGORY_APPLICATION_STATUS)
		self.ind.set_status(appindicator.STATUS_ATTENTION)

		self.ind.set_label("Getting data...")
		gobject.timeout_add(5000, self.update_label)

		self.menu_setup()
		self.ind.set_menu(self.menu)
		gtk.main()


	def menu_setup(self):
		self.menu = gtk.Menu()

		self.quit_item = gtk.MenuItem("Quit")
		self.quit_item.connect("activate", self.quit)
		self.quit_item.show()
		self.menu.append(self.quit_item)


	def get_data(self):
		conn = sqlite3.connect(sqlite_db)
		c = conn.cursor()
		count = 0;
		for row in c.execute("SELECT jsonAttributes FROM messages WHERE folderID=1"):
			if row[0]:
				if row[0].find('"58":false') > -1:
					count += 1

		return count


	def update_label(self):
		str_to_display = " Inbox: " + str(self.get_data())

		self.ind.set_label(str_to_display)
		return True


	def quit(self, widget):
		sys.exit(0)


if __name__ == "__main__":
	indiCator = Thunderbird()
	
