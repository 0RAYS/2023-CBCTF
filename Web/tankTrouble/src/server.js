const Player_1 = require("./server/Player");
const express = require('express');const app = express();
const server = require('http').createServer(app);
const FLAG = {flag: process.env.FLAG || "flag{no_flag}"}
app.get('/', function (req, res) {
    res.sendFile(__dirname + '/client/index.html');
});
app.get('/*', function (req, res) {
    var file = req.params[0];
    // console.log('\t :: Express :: file requested : ' + file);
    res.sendFile(__dirname + "/client/" + file);
});
server.listen(process.env.PORT || 3000);
console.log("Server started on localhost:3000");
const io = require('socket.io')(server, {});
var ALL_SOCKETS = {};
var ALL_PLAYERS = {};
var ADDRESS = [];
io.on('connect', function (socket) {
    let addr = socket.handshake.address;
    if(ADDRESS.includes(addr)) {
        ADDRESS.splice(ADDRESS.indexOf(addr),1);
        delete ALL_SOCKETS[addr];
        delete ALL_PLAYERS[addr];
    }
    console.log(addr);
    ALL_SOCKETS[addr] = socket;
    ADDRESS.push(addr);
    var player;
    socket.on("start", function (data) {
        player = new Player_1.Player(addr, data.name);
        console.log("Recieved Name:", data.name);
        // tell the client their own id and the rest of the player
        socket.emit("serverState", {
            id: addr,
            otherPlayers: ALL_PLAYERS
        });
        ALL_PLAYERS[addr] = player;
        // tell everyone else that their is a new player
        socket.broadcast.emit("newPlayer", {
            id: addr,
            newPlayer: player,
            name: data.name
        });
    });
    socket.on("position", function (data) {
        if(data) {
            try {
                ALL_PLAYERS[addr].x = data.x;
                ALL_PLAYERS[addr].y = data.y;
                ALL_PLAYERS[addr].r = data.r;
                ALL_PLAYERS[addr].health = data.health;
            } catch(e) {
            }
            // console.log("ID:", addr, "Received health:", data.health);
        }
    });
    socket.on('shoot', function (data) {
        socket.broadcast.emit('shoot', { id: addr });
    });
    socket.on('kill', function (data) {
        if(data) {
            try {
                let id = data.killer;
                if(id) {
                    ALL_PLAYERS[id].score += 1;
                }
                socket.broadcast.emit('killBroadcast', {
                    killer: id? ALL_PLAYERS[id].name : ALL_PLAYERS[addr].name,
                    killed: id? ALL_PLAYERS[addr].name : "自己"
                });
            } catch(e) {
            }
        }
    });
    socket.on("getFlag", function (data) {
        try {
        // console.log(ALL_PLAYERS[addr].score);
            if(ALL_PLAYERS[addr].score >= 555) {
                ALL_PLAYERS[addr].score -= 555;
                socket.emit("getFlag", FLAG);
            } else {
                socket.emit("getFlag", {flag: "玩够555分就能拿到flag"});
            }
        } catch(e) {
        }
    });
    socket.on("disconnect", function () {
        try {
            delete ALL_SOCKETS[addr];
            delete ALL_PLAYERS[addr];
            ADDRESS.splice(ADDRESS.indexOf(addr),1);
            socket.broadcast.emit("removed", {
                id: addr
            });
            console.log("Socket disconnected:", addr);
        } catch(e) {}
    });
});
setInterval(function () {
    var pack = {};
    try{
        for (var i in ALL_PLAYERS) {
            var player;
            player = ALL_PLAYERS[i];
            pack[i] = {
                x: player.x,
                y: player.y,
                r: player.r,
                health: player.health,
                score: player.score
            };
        }
        for (var i in ALL_SOCKETS) {
            var socket = ALL_SOCKETS[i];
            socket.emit("update", pack);
        }
    } catch(e){}
}, 100);
// setInterval(function () {
//     console.log("Debug Info:");
//     for (var i in ALL_PLAYERS) {
//         let p = ALL_PLAYERS[i];
//         console.log("id:", p.id);
//         // console.log(p.bulletInfo);
//     }
// }, 2000);
