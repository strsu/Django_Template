class ReceiveManager {
    constructor(box) {
        this.box = box;
    }

    actor(data) {
        if (data.info) {
            this.userCount(data.info);
        } else if (data.msg) {
            this.insertChat(data.msg);
        } else if (data.food) {
            this.insertChat(data.msg);
            //msg.food(data.food);
        }
    }

    userCount(data) {
        document.getElementById('chat-user').innerText = `현재 접속 인원: ${data.user_cnt}`;
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

    insertChat(data) {
        let log = document.querySelector(this.box);

        let chat = document.createElement("div");
        let usr = document.createElement("div");
        let msg_container = document.createElement("div");
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

        const now = new Date(data.time);
        const hours = now.getHours().toString().padStart(2, 0);
        const minutes = now.getMinutes().toString().padStart(2, 0);
        time.innerText = `${hours}:${minutes}`;
        time.style.fontSize = "13px";

        chat.appendChild(usr);

        if (data.image) {
            let img = document.createElement("img");
            img.src = data.image;
            img.id = "chat-img";
            img.name = this.generateRandomString(10);
            img.setAttribute("onclick", `openModal("${img.name}")`);
            chat.appendChild(img);

            if (!data.message) {
                img.appendChild(time);
            }
        }

        if (data.message) {
            msg_container.appendChild(msg);
            msg_container.appendChild(time);
            chat.appendChild(msg_container);
        }
        log.appendChild(chat);
        log.scrollTop = log.scrollHeight + log.clientHeight; // msg오면 제일 하단으로 이동
    }

}