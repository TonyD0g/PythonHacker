<?php


//verify : 过滤函数
function verify($str,$kind=''){
if(empty($str)){return 'error';}
if($kind=='username') {
            Return preg_match("/^[A-Za-z0-9_\x{4e00}-\x{9fa5}]{2,32}$/u",$str);
        }
    }
//path1 : 引入的字典
//path2 : 输出的结果
$path = "D:\Coding\pyhton\PythonHacker\Python随想\Web\简单小工具\Ascii.txt";
$path1 = "D:\Coding\pyhton\PythonHacker\Python随想\Web\简单小工具\FuzzOut.txt";
$file = fopen($path, "r");
$file1 = fopen($path1,'w');
$i=0;
if ($file==NUll)
{
    print('$file is not find');
    exit(0);
}
if ($file1==NUll)
{
    print('$file1 is not find');
    exit(0);
}
//输出文本中所有的行，直到文件结束为止。
while(! feof($file))
{
    
$str= fgets($file);//fgets()函数从文件指针中读取一行 
$i++;
$outcome = verify($str,'username');
if(!empty($str))
if($outcome==$str)
// print($i.':'.$str);
$string = $i.':'.$str;
fwrite($file1,$string);
}
print('[+]  Success!');
fclose($file);

?> 