use Irssi;

$log_file = '/home/bart/.irssi/log.txt';

open (MYFILE, '>>' . $log_file);
print MYFILE "Started...\n";
close (MYFILE);

sub event_handle {
	# $data = "nick/#channel :text"
	my ($server, $data, $nick, $address) = @_;
	open (MYFILE, '>>' . $log_file);
	print MYFILE $nick . ": " . $data . "\n";
	close (MYFILE);
}

Irssi::signal_add("message public", "event_handle")


# put the file in ~/.irssi/scripts
# and run in your irssi the following command: 
# /run irssi_notify
# 

# "message public", SERVER_REC, char *msg, char *nick, char *address, char *target
# "message private", SERVER_REC, char *msg, char *nick, char *address
