<?php
$url = 'url=http://127.0.0.1111;echo `cat f*`>1.txt;11/a';
$url = parse_url($url);
var_dump($url)
?>