class GameState extends Phaser.State {
    constructor() {
        super();
        this.otherPlayers = {};
    }
    init(name) {
        this.name = name;
    }
    preload() {
    }
    create() {
        this.socket = io();
        this.otherGroup = this.game.add.group();
        this.randomGenerator = new Phaser.RandomDataGenerator();
        this.game.stage.backgroundColor = '#dfdfdf';
        this.map = this.game.add.tilemap('map');
        this.map.addTilesetImage('tiles');
        this.layer = this.map.createLayer("Tile Layer 1");
        this.layer.resizeWorld();
        this.map.setCollision([33]);
        this.tank = new Tank(this.game, 400, 400, this.name, this.id, this.socket);
        this.game.add.existing(this.tank);
        this.game.camera.follow(this.tank);
        this.socket.emit("start", { name: this.name });
        this.socket.on("serverState", this.onServerState.bind(this));
        this.socket.on("newPlayer", this.onNewPlayer.bind(this));
        this.socket.on("removed", this.onRemoved.bind(this));
        this.socket.on("update", this.onUpdate.bind(this));
        this.socket.on("shoot", this.onShoot.bind(this));
        this.socket.on("killBroadcast", this.killBroadcast.bind(this));
        this.socket.on("getFlag", data => alert(data.flag));
        document.getElementById("flag").addEventListener("click", () => this.socket.emit("getFlag"));
        this.notice = document.getElementById("notice");
    }
    update() {
        this.socket.emit('position', {
            x: this.tank.x,
            y: this.tank.y,
            r: this.tank.rotation,
            id: this.id,
            health: this.tank.health,
        });
        ////////////////////////////////////// handle all collisions ///////////////////////////////////////////
        // tank-with walls
        this.game.physics.arcade.collide(this.tank, this.layer);
        // otherTanks with walls
        this.game.physics.arcade.collide(this.otherGroup, this.layer);
        // tank bullets with walls
        this.game.physics.arcade.collide(this.tank.weapon.bullets, this.layer);
        // otherTanks bullets with walls
        this.otherGroup.forEach(function (t) {
            this.game.physics.arcade.collide(t.weapon.bullets, this.layer);
        }, this);
        // tank with it's own bullets
        this.game.physics.arcade.collide(this.tank, this.tank.weapon.bullets, (tank, bullet) => {
            bullet.kill();
            tank.health -= 1;
            // console.log("I shot myself.");
            if (tank.health <= 0) {
                updateContent(this.notice.children[3], "you have been slain by yourself");
                // this.notice.children[3].textContent = "you have been slain by yourself";
                // console.log("you have been slain by yourself");
            }
        });
        // otherTanks with their own bullets
        this.otherGroup.forEach(function (t) {
            this.game.physics.arcade.collide(t, t.weapon.bullets, (tank, bullet) => {
                bullet.kill();

            });
        }, this);
        // tank bullets with otherTanks
        this.otherGroup.forEach(function (t) {
            this.game.physics.arcade.collide(t, this.tank.weapon.bullets, (tank, bullet) => {
                bullet.kill();

            });
        }, this);
        // otherTanks bullets with me
        this.otherGroup.forEach(function (t) {
            this.game.physics.arcade.collide(this.tank, t.weapon.bullets, (tank, bullet) => {
                bullet.kill();
                tank.health -= 1;
                if (tank.health <= 0) {
                    tank.socket.emit("kill", {
                        killer: t.id
                    });
                    updateContent(this.notice.children[3], `you have been slain by ${t.name}`);
                }
            });
        }, this);
    }
    onShoot(data) {
        this.otherPlayers[data.id].weapon.fire();
    }
    onServerState(data) {
        this.id = data.id;
        for (var x in data.otherPlayers) {
            var p = data.otherPlayers[x];
            var t = new otherTank(this.game, p.x, p.y, p.id, p.name);
            this.otherPlayers[x] = t;
            // this.tank.addNewPlayer(t);
            this.otherGroup.add(t);
        }
    }
    onNewPlayer(data) {
        var t = new otherTank(this.game, data.newPlayer.x, data.newPlayer.y, data.id, data.name);
        this.otherPlayers[data.id] = t;
        // this.tank.addNewPlayer(t);
        this.otherGroup.add(t);
    }
    onRemoved(data) {
        this.otherPlayers[data.id].displayName.destroy();
        this.otherPlayers[data.id].weapon.bullets.destroy();
        this.otherPlayers[data.id].healthBar.kill();
        this.otherPlayers[data.id].destroy();
        delete this.otherPlayers[data.id];
    }
    onUpdate(data) {
        // console.log("Everyone else's info:");
        this.notice.children[0].textContent = `当前房间玩家数量：${Object.keys(data).length}`;
        for (var i in data) {
            var x, y, r, id, health;
            if (i != this.id) {
                x = data[i].x;
                y = data[i].y;
                r = data[i].r;
                id = data[i].id;
                health = data[i].health;
                if (this.otherPlayers[i] == null) {
                    console.log("Player is null.");
                }
                else {
                    this.otherPlayers[i].updateInfo(x, y, r, health);
                }
            }else {
                this.notice.children[1].textContent = `当前得分：${data[i].score}`;
            }
        }
    }
    killBroadcast(data) {
        let id = data.id;
        let killer = data.killer;
        let killed = data.killed;
        updateContent(this.notice.children[3], `${killer} 干掉了 ${killed}`);
        // console.log(`${killer} 干掉了 ${killed}`);
    }
}
function updateContent(div, text) {

    div.classList.remove("fadeIn");
    div.classList.add("fadeOut");
    setTimeout(function(){
      div.textContent = text;
      div.classList.remove("fadeOut");
      div.classList.add("fadeIn");
    }, 500);
}
