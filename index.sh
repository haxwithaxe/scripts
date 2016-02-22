#!/bin/bash
# generate an html index of a directory
#
# Arguments:
#	$1 (optional): Path to create the index.html relative to.
#   $2 (optional): Email address of takedown contact.
#
# Outputs:
#	STDOUT: HTML index of files in $path
#

path=${1:-$PWD}
email_address=${2:-${USER}@$(hostname -f)}

cat - <<EOHTML
<html>
<body>
<h1>Index of files</h1>
<div>Static index of files created with \`$0\`</div>
<div>Remove if desired. Email $email_address if this directory must not be indexed.</div>
<table class="table table-striped table-condensed">
EOHTML

find $path -maxdepth 1 -regex "[.]*[/]*[^.]*" -printf '<tr><td><a href="%f">%f</a></td><td>%TY-%Tm-%Td %TH:%TM</td><td>%s</td>\n'

cat - <<EOHTML
</br>
</br>
</body>
</html>
EOHTML
