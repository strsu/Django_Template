class WebSocketManager {
    constructor(path, receiver, userName) {
        this.receiver = receiver;
        this.userName = userName;
        this.path = path;
        this.socket = new WebSocket(path);
        this.socket.onopen = this.onopen.bind(this);
        this.socket.onerror = this.onopen.bind(this);
        this.socket.onmessage = this.onmessage.bind(this);
        this.socket.onclose = this.onclose.bind(this);
    }

    getReadyState() {
        return this.socket.readyState
    }

    connect() {
        this.socket = new WebSocket(this.path);
        this.socket.onopen = this.onopen.bind(this);
        this.socket.onerror = this.onopen.bind(this);
        this.socket.onmessage = this.onmessage.bind(this);
        this.socket.onclose = this.onclose.bind(this);
    }

    onopen(event) {
        //console.log('WebSocket connection opened:', event);
        document.getElementById("chat-message-input").removeAttribute("readonly");
        //document.getElementById("chat-message-input").focus();
        //document.addEventListener('mousemove', getMousePosition);
    }

    onmessage(event) {
        const data = JSON.parse(event.data);
        this.receiver.actor(data);
    }

    onerror(event) {
        console.log('WebSocket connection error:', event);
    }

    onclose(event) {
        console.log("Socket closed with code:", event.code, "reason:", event.reason);
    }

    send(data) {
        if (this.socket.readyState == 1) {
            this.socket.send(data);
        }

        if (this.socket.readyState > 1) {
            this.connect();
        }

    }

    sendText(message) {
        let base = {
            'name': this.userName,
            "time": new Date()
        }

        let data = {
            "data": Object.assign({}, base, message)
        }
        this.send(JSON.stringify(data));
    }

    sendBytes(data) {
        this.send(data);
    }

}


