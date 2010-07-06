<?php
$ipaddr = "" ;
$sedexec0 = "echo $ipaddr | cut -d . -f1";
$sed0 = exec($sedexec0);

$sedexec1 = "echo $ipaddr | cut -d . -f2";
$sed1 = exec($sedexec1);

$sedexec2 = "echo $ipaddr | cut -d . -f3";
$sed2 = exec($sedexec2);

$ip_start = ( $sed0 * 256 + $sed1 ) * 256 + $sed2 ;

$link = mysql_connect('localhost', 'mysql_user', '^^y*ql');
if (!$link) {
   die('Could not connect: ' . mysql_error());
}
//echo "Connected Successfully\n" ;

mysql_select_db("ipinfodb");

$query = 'SELECT * FROM ip_group_city WHERE ip_start = "$ip_start"' ;

$result = mysql_query($query);
echo "$ipaddr  ";
echo mysql_result($result, 0, 1);
echo ".";
echo mysql_result($result, 0, 2);
echo ".";
echo mysql_result($result, 0, 3);
echo ".";
echo mysql_result($result, 0, 4);

mysql_free_result($result);

mysql_close($link);
?>