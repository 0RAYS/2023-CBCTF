主要文件：auto_mmmmmultiply.py
执行 python auto_mmmmmultiply.py以生成tricode脚本。
生成结果：mmmmmultiply.bin
中间产物：mmmmmultiply.src, mmmmmultiply.tribc, mmmmmultiply.tricode
注意：生成有随机性

TIVM_integrated文件夹内有visual studio工程，内容为C语言的TIVM解释器以及TIVM脚本的二进制代码。有编译样本TIVM_integrated.exe
注意：修改TIVM脚本需要手动填充mmmmmultiply.bin 到TIVM_integrated.cpp
secret.py内有flag

库文件：
lib/tri_inst_compiler.py	TIVM编译器
gen_putstr.py			TIVM脚本字符串输出
bin_interface.py		tricode脚本/二进制转换
