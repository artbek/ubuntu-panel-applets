top.py
======
- shows top 2 processes


thunderbird.py
==============
- shows number of unread messages in your Thunderbird Inbox
- make sure to edit this line (it should point to your Thunderbird database file):
	sqlite_db = "/home/bart/.thunderbird/ug524fiy.default/global-messages-db.sqlite"



Launch at startup
=================

Put below in your ~/.xsession file, to launch the applets at startup:

python [path]/top.py &
python [path]/thunderbird.py &

