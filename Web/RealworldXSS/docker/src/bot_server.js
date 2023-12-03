const puppeteer = require("puppeteer");
const cors = require('cors');
const fs = require('fs');
const https = require('https');
const FLAG = process.env.FLAG || "flag{*** REDACTED ***}";
const sleep = async (s) => new Promise((resolve) => setTimeout(resolve, s));


let running = false
const check = async (cookies) => {

    running = true

	console.log(cookies);

	let browser;
	try {
		browser = await puppeteer.launch({
			headless: true,
			args: [
				"--js-flags=--noexpose_wasm,--jitless",
				"--no-sandbox"
			],
			executablePath: "/usr/bin/chromium-browser",
            // executablePath: "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe",
		});

		const context = await browser.createIncognitoBrowserContext();
		const page1 = await context.newPage();
        const page2 = await context.newPage();


        await page1.goto('https://i.hdu.edu.cn')

        await cookies.split(';').forEach((cookie)=>{
            console.log({name: cookie.split('=')[0].trimLeft(),
                value: cookie.split('=')[1].trimLeft()})
            page1.setCookie({
                name: cookie.split('=')[0].trimLeft(),
                value: cookie.split('=')[1].trimLeft(),
                domain: 'i.hdu.edu.cn',
                path: '/',
                expires: Date.now() + 86400 * 1000,
                httpOnly: true,
                secure: false,
            })
        })
        page1.setCookie({
            name: 'flag',
            value: FLAG,
            domain: 'i.hdu.edu.cn',
            path: '/',
            expires: Date.now() + 86400 * 1000,
            httpOnly: false,
            secure: false,
        })
        await sleep(1000);
        await page2.goto('https://i.hdu.edu.cn/mnews/_web/_ids/user/api/userInfo/edit0.rst?act=control&_p=YXM9MA__')
        await sleep(10000);
        
		await browser.close();

	} catch (e) {
		console.log(e);

	} finally {
		if (browser) await browser.close();
        running = false;
	}
};

const app = require("express")();
app.use(cors());

// 配置 SSL 选项
const sslOptions = {
    key: fs.readFileSync('./key.pem'),
    cert: fs.readFileSync('./certificate.pem')
  };
  
  // 创建 HTTPS 服务器
const server = https.createServer(sslOptions, app);

app.get('/', (req, res) => {
    console.log('start');
    if(!req.query.cookie || req.query.cookie == undefined){
	res.end('missing param')
    }
    else{
        if(running) res.end('the last request still running')
        try{
            res.end('checking.')
            check(decodeURIComponent(req.query.cookie));
        }catch(e){
            res.status(404).end('Error Occured')
        }    
    }
})

server.listen(3000,()=>{
	console.log('listening at port 3000')
});

