主要文件：auto_traceme.py
执行 python auto_traceme.py以生成tricode脚本。
生成结果：traceme.bin
中间产物：traceme.tribc, traceme.tricode
注意：生成有随机性

TIVM_run文件夹内有visual studio工程，内容为C语言的TIVM解释器。有编译样本TIVM_run.exe。
secret.py内有flag

库文件：
lib/tri_inst_compiler.py	TIVM编译器
gen_putstr.py			TIVM脚本字符串输出
bin_interface.py		tricode脚本/二进制转换
