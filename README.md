top.py
======
- shows top 2 processes


thunderbird.py
==============
- shows number of unread messages in your Thunderbird Inbox
- make sure to edit the line (it should point to your Thunderbird database file):
	<code>sqlite_db = "/home/bart/.thunderbird/ug524fiy.default/global-messages-db.sqlite"</code>



Launch at startup
=================

Put below in your ~/.xsession file, to launch the applets at startup:

<code>python [path]/top.py &</code>

<code>python [path]/thunderbird.py &</code>
