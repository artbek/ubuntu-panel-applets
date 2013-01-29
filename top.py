#!/usr/bin/env python
import sys
import gtk
import appindicator

import subprocess
import re
import gobject


class Top:
	def __init__(self):
		self.ind = appindicator.Indicator("new-mail-indicator",
										   "",
										   appindicator.CATEGORY_APPLICATION_STATUS)
		self.ind.set_status(appindicator.STATUS_ACTIVE)

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


	def get_data(self, line_number = 1):
		command = "top -b | head -" + str(7 + line_number) + " | tail -1"
		r = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
		data = r.communicate()[0]
		data = re.sub(r' +', r' ', data.strip()).split(" ")
		str_to_display = data[11] + " - [" + data[8] + "%]"

		return str_to_display


	def update_label(self):
		str_to_display = self.get_data(1) + " .. " + self.get_data(2)

		self.ind.set_label(str_to_display)
		return True


	def quit(self, widget):
		sys.exit(0)


if __name__ == "__main__":
	indiCator = Top()
