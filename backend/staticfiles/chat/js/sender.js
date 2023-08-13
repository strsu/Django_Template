class SendManager {
    constructor(socketManager) {
        this.socketManager = socketManager;
        this.canvas = document.getElementById('myCanvas');
        this.canvas.addEventListener('click', this.onmouseclick.bind(this));
        this.ctx = this.canvas.getContext('2d');
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

        document.querySelector('#moving-text').onkeyup = function(e) {
            if (e.keyCode === 13) {  // enter, return
                const messageInputDom = document.querySelector('#moving-text');
                const message = messageInputDom.value;
                if (!message) {
                    return;
                }
                socketManager.sendText({
                    'message': message,
                })
                messageInputDom.value = '';
            }
        };
    }
}