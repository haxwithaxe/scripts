#!/bin/bash
# generate an html index of a directory
echo '<html>'
echo '<body>'
echo '<h1>Index of files</h1>'
ls -1 . | sed /^index.html$/d | sed 's:^.*:<a href=\"&\">&</a><br>:g'
echo '<br>'
echo '<br>'
echo '</body>'
echo '</html>'
exit 0
