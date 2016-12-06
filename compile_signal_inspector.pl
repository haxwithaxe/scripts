use strict;

'Copyright (C) 2016, haxwithaxe <spam@haxwithaxe.net>
License GPLv3 http://www.gnu.org/licenses/gpl.html
This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.';


my $irssi_script_base = "use strict;
use Irssi;

use vars qw(\$VERSION %IRSSI);

\$VERSION = '0.1';

";

sub add_signal {
	my $signal = shift; 
	my $handler = $signal;
	$handler =~ s/ /_/g;
	my $signal_add = "Irssi::signal_add( \"".$signal."\", \"".$handler."\" );";
	my $signal_handler = "sub ".$handler." {
	my \$args = join(\", \", \@_);
	Irssi::print(\"".$signal.">>>\".\$args);
}\n";
	print "\n# handle ".$signal."\n".$signal_handler.$signal_add."\n";
}

print $irssi_script_base;

add_signal("message public");
# $server, $msg, $nick, $address, $target

add_signal("message private");
# $server, $msg, $nick, $address

add_signal("message own_public");
# $server, $msg, $target

add_signal("message own_private");
# $server, $msg, $target, $original_target

