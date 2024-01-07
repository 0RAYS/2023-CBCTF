<?php 
error_reporting(0);    
if($_SERVER['REQUEST_METHOD']==='POST') {
    
    $filename = $_FILES['file']['name'];
    $tmp_name = $_FILES['file']['tmp_name'];
    $size = $_FILES['file']['size'];
    $error = $_FILES['file']['error'];
    if ($size > 2*1024*1024){
        echo "too larage";
        exit();
    }
    
    $arr = pathinfo($filename);
    $ext_suffix = $arr['extension'];
    $allow_suffix = array('jpg','gif','jpeg','png');
    if(!in_array($ext_suffix, $allow_suffix)){  
        echo "only jpg,gif,jpeg,png";
        exit();
    }
    
    $new_filename = date('YmdHis',time()).rand(100,1000).'.'.$ext_suffix; 
    if(!is_dir("upload")) {
        mkdir("upload");
    }
    if(move_uploaded_file($tmp_name, 'upload/'.$new_filename)) {
        echo "success save in: ".'upload/'.$new_filename;
    } else {
        echo "upload error!";
    }

} else if ($_SERVER['REQUEST_METHOD']==='GET') {
    if (isset($_GET['ccc'])){
        include("f71fade1b8ed74a6d9849359380b760e.php");
        $fpath = $_GET['ccc'];
        if(file_exists($fpath)){
            echo "file exists";
        } else { 
            echo "file not exists";
        }
    } else if(isset($_GET['orz'])) {
        $jbn1 = $_GET['jbn1'];
        $jbn2 = $_GET['jbn2'];
        if ($jbn1 !== $jbn2 && md5($jbn1) == md5($jbn2)){
            $usernamne = $_GET["username"];
            $password = $_GET["password"];
            if($usernamne === "0rays" && $password !== "Array" && md5("0raysArray") === md5($usernamne.$password)) {
                //now you can
                echo file_get_contents("f71fade1b8ed74a6d9849359380b760e.php");
            } else {
                echo "no~~~~~";
            }
        }
    } else {
        highlight_file(__FILE__);
    } 
}  
?>