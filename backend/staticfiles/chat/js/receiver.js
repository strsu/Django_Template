class ReceiveManager {
    constructor(box) {
        this.box = box;
        this.canvas = document.getElementById('myCanvas');
        this.canvas.addEventListener('click', this.onmouseclick.bind(this));
        this.ctx = this.canvas.getContext('2d');
        this.user = {};
        this.color = ["#FFB6C1", "#00FF7F", "#8A2BE2", "#FFD700", "#00BFFF", "#FFA07A", "#00FA9A", "#9932CC", "#FF69B4", "#00CED1", "#FF8C00", "#48D1CC", "#FF1493", "#00FFFF", "#FF4500", "#40E0D0", "#FF00FF", "#7B68EE", "#FF6347", "#00FFFF"];
    }

    actor(data) {
        if (data.info) {
            if (data.info.percent) {
                this.fileUploadPercent(data.info);
            } else if (data.info.user_cnt) {
                this.userCount(data.info);
            }
        } else if (data.msg) {
            this.insertChat(data.msg);
        } else if (data.food) {
            this.insertChat(data.food);
            //msg.food(data.food);
        } else if (data.mouse) {
            this.drawMouse(data.mouse);
        }
    }

    userCount(data) {
        document.getElementById('chat-user').innerText = `현재 접속 인원: ${data.user_cnt}`;
    }

    fileUploadPercent(data) {
        let progressBar = document.getElementById('progressBar');
        if (progressBar.value == 100) {
            progressBar.value = 0;
        }
        progressBar.value = data.percent;
    }

    generateRandomString(length) {
        let result = '';
        const characters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
        const charactersLength = characters.length;
        for (let i = 0; i < length; i++) {
            result += characters.charAt(Math.floor(Math.random() * charactersLength));
        }
        return result;
    }

    timeParser(time) {
        const now = new Date(time);
        const hours = now.getHours().toString().padStart(2, 0);
        const minutes = now.getMinutes().toString().padStart(2, 0);
        return `${hours}:${minutes}`;
    }

    boxMaker(data) {
        let chat = document.createElement("div");
        let msg_container = document.createElement("div");

        let usr = document.createElement("div");
        let msg = document.createElement("div");
        let time = document.createElement("div");

        if (data.flag) {
            chat.id = "msg-container-my";
            msg_container.id = "msg-inner-container-my";
            msg.id = "msg-msg-my";
        } else {
            chat.id = "msg-container";
            msg_container.id = "msg-inner-container";
            msg.id = "msg-msg";
        }

        usr.id = "msg-usr";
        usr.innerText = data.name;
        msg.innerText = data.message;

        time.innerText = this.timeParser(data.time);
        time.style.fontSize = "13px";

        msg_container.appendChild(msg);
        msg_container.appendChild(time);
        chat.appendChild(usr);

        this.chat = chat;
        this.msg_container = msg_container;
    }

    insertChat(data) {
        let log = document.querySelector(this.box);
        this.boxMaker(data);


        if (data.image) {
            let img = document.createElement("img");
            img.src = data.image;
            img.id = "chat-img";
            img.name = this.generateRandomString(10);
            img.setAttribute("onclick", `modal.open('${img.name}')`);
            this.chat.appendChild(img);
        }

        if (data.message) {
            this.chat.appendChild(this.msg_container);
        }
        log.appendChild(this.chat);
        log.scrollTop = log.scrollHeight + log.clientHeight; // msg오면 제일 하단으로 이동
    }

    onmouseclick(event) {
        const x = event.clientX - this.canvas.offsetLeft;
        const y = event.clientY - this.canvas.offsetTop;
        let box = document.getElementById("moving-text");
        if (box) {
            box.remove();
        }
        const textbox = document.createElement("input");
        textbox.type = "text";
        textbox.id = "moving-text";
        textbox.style.position = "absolute";
        textbox.style.left = x + "px";
        textbox.style.top = y + "px";
        textbox.style.width = "200px";
        document.body.appendChild(textbox);
    }

    drawMouse(data) {
        let ctx = this.ctx;
        this.canvas.width = window.innerWidth;
        this.canvas.height = window.innerHeight;

        function drawCircle(x, y, user, color) {
            ctx.beginPath();
            ctx.arc(x, y, 10, 0, Math.PI * 2);
            ctx.fillStyle = color;
            ctx.fill();
            ctx.closePath();

            // 원 옆에 이름 출력하기
            ctx.fillStyle = "white";
            ctx.font = "12px sans-serif";
            ctx.fillText(user, x, y - 15);
        }

        function clearCanvas() {
            //ctx.clearRect(0, 0, canvas.width, canvas.height);
        }

        this.user[data.name] = data.mouse;
        const entries = Object.entries(this.user);
        entries.map(([user, value], index) => {
            let mouse = value;
            let color = this.color[index];
            drawCircle(mouse[0], mouse[1], user, color);
        });

        for (const [user, value] of Object.entries(this.user)) {

        }
    }
}