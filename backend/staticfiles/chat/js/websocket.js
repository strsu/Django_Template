class WebSocketManager {
    constructor(path, receiver, userName) {
        this.receiver = receiver;
        this.userName = userName;
        this.socket = new WebSocket(path);
        this.socket.onopen = this.onopen.bind(this);
        this.socket.onmessage = this.onmessage.bind(this);
        this.socket.onclose = this.onclose.bind(this);
    }

    onopen(event) {
        console.log('WebSocket connection opened:', event);
    }

    onmessage(event) {
        const data = JSON.parse(event.data);
        this.receiver.actor(data);
    }

    onclose(event) {
        console.log('WebSocket connection closed:', event);
    }

    sendText(message) {
        let base = {
            'name': this.userName,
            "time": new Date()
        }

        let data = {
            "data": Object.assign({}, base, message)
        }

        this.socket.send(JSON.stringify(data));
    }

    sendBytes(data) {
        this.socket.send(data);
    }
}


