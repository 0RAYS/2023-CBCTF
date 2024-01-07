<?php

error_reporting(0);

class Act {
    protected $checkAccess;
    protected $id;

    public function run()
    {  
        
        if ($this->id !== 0 && $this->id !== 1) {
            switch($this->id) {
                case 0:
                    if ($this->checkAccess) {
                        
                        include($this->checkAccess);
                    }
                    break;
                case 1:
                    throw new Exception("id invalid in ".__CLASS__.__FUNCTION__);
                    break;
                default:
                    break;         
            }
        }
    }

}

class Con {

    public $formatters;
    public $providers;

    public function getFormatter($formatter)
    {
        if (isset($this->formatters[$formatter])) {
            return $this->formatters[$formatter];
        }
    
        foreach ($this->providers as $provider) {
            if (method_exists($provider, $formatter)) {
                $this->formatters[$formatter] = array($provider, $formatter);
                return $this->formatters[$formatter];
            }
        }
        throw new \InvalidArgumentException(sprintf('Unknown formatter "%s"', $formatter));
    }

    public function __call($name, $arguments)
    {
        return call_user_func_array($this->getFormatter($name), $arguments);
    }
}

class Mmm {

    public function __invoke(){
        include("hello.php");
    }
}

class Jbn{
    public $source;
    public $str;
    public $reader;

    public function __wakeup() {
        
        if(preg_match("/gopher|phar|http|file|ftp|dict|\.\./i", $this->source)) {
            throw new Exception('invalid protocol found in '.__CLASS__);
        }
    }

    public function __construct($file='index.php') {
        $this->source = $file;
        echo 'Welcome to '.$this->source."<br>";
    }
    public function __toString() {
        
        
        $this->str->reset();
    }


    public function reset() {
        if ($this->reader !== null) {
            
            
            $this->reader->close();
        }
    }
}