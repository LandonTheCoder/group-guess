#
# Regular cron jobs for the group-guess package
#
0 4	* * *	root	[ -x /usr/bin/group-guess_maintenance ] && /usr/bin/group-guess_maintenance
