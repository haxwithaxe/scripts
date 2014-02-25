<?php
	print('Content-Type: text/plain\n\n');

    if (!empty($_SERVER['HTTP_CLIENT_IP'])) //if from shared
    {
        print($_SERVER['HTTP_CLIENT_IP']);
    }
    else if (!empty($_SERVER['HTTP_X_FORWARDED_FOR']))   //if from a proxy
    {
        print($_SERVER['HTTP_X_FORWARDED_FOR']);
    }
    else
    {
        print($_SERVER['REMOTE_ADDR']);
    }

?>
