import express from 'express';

// Allow deserialization of functions
// which's not part of the challenge
// see https://github.com/nodeca/js-yaml/blob/3.14.1/README.md#load-string---options- for details
import pkg from 'js-yaml'; const { load } = pkg;
import path from 'path';


const app = express();
const __dirname = path.resolve();
const test = async (data) => {
    return load(data);
}


app.use('/', express.static(`${__dirname}/static`))
.all("/", express.urlencoded(), async (req, res) => {
    let { data } = req.body;
    if (data) {
        try {
            await test(data);
            res.sendFile(`${__dirname}/html/good.html`);
        } catch(e) {
            console.log(e)
            res.sendFile(`${__dirname}/html/baad.html`);
        }
    } else res.sendFile(`${__dirname}/html/index.html`);

}).listen(1337);


