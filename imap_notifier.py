#!/usr/bin/env python
import sys
import gtk
import appindicator

import gobject
import imaplib
import time

# Helpful sometimes to reload the panel:
#     killall unity-panel-service

# Example config file:
#     user = xxx
#     password = xxx
#     server = xxx
#     port = 1
#     mailboxes = INBOX,INBOX/spam
#     log_file = /home/.../imap_notifier.log

# To run, e.g.:
# python imap.py <config_file_path> &


class Imap:

	config = {
		'user': 'xxx',
		'password': 'xxx',
		'server': 'xxx',
		'port': 1,
		'mailboxes': 'INBOX',
		'log_file': '',
	}


	def __init__(self):
		if (len(sys.argv) < 2):
			print('Config file not given!')
			sys.exit()

		config_file = open(sys.argv[1], 'r')
		for line in config_file:
			if (len(line.split('=')) == 2):
				(key, value) = line.split('=')
				self.config[key.strip()] = value.strip()

		config_file.close()

		self.ind = appindicator.Indicator(
			"new-mail-indicator",
			"",
			appindicator.CATEGORY_APPLICATION_STATUS
		)
		self.ind.set_status(appindicator.STATUS_ACTIVE)

		self.ind.set_label("Getting outlook365 data...")
		self.ind.set_icon("indicator-messages")
		self.ind.set_attention_icon("indicator-messages-new")

		gobject.timeout_add(10000, self.update_label)

		self.menu_setup()
		self.ind.set_menu(self.menu)
		gtk.main()


	def menu_setup(self):
		self.menu = gtk.Menu()
		self.quit_item = gtk.MenuItem("Quit")
		self.quit_item.connect("activate", self.quit)
		self.quit_item.show()
		self.menu.append(self.quit_item)


	def log(self, message):
		if self.config['log_file']:
			with open(self.config['log_file'], "a") as log_file:
				log_file.write(message + '\n')
				log_file.close()


	def get_data(self):
		messages_count = 0

		try:
			conn = imaplib.IMAP4_SSL(self.config['server'], self.config['port'])
			conn.login(self.config['user'], self.config['password'])

			mailboxes = self.config['mailboxes'].split(',')

			for mailbox in mailboxes:
				conn.select(mailbox, readonly = 1)
				(status, messages) = conn.search(None, '(UNSEEN)')

				log_message = time.strftime("%d/%m/%Y %I:%M:%S %p")
				log_message += " (" + mailbox + "): " + status + " - " + str(messages)

				self.log(log_message)

				if status == 'OK':
					if len(messages[0]):
						messages_count += len(messages[0].split(' '))

			conn.close()

		except:
			self.log(str(sys.exc_info()))
			pass

		return messages_count


	def update_label(self):
		messages_count = self.get_data()

		if messages_count:
			self.ind.set_status(appindicator.STATUS_ATTENTION)
		else:
			self.ind.set_status(appindicator.STATUS_ACTIVE)

		str_to_display = " Inbox: " + str(messages_count)
		str_to_display += " ( " + time.strftime("%I:%M %p") + " ) "
		self.ind.set_label(str_to_display)

		return True


	def quit(self, widget):
		sys.exit(0)


if __name__ == "__main__":
	indiCator = Imap()

