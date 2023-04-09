class FileManager {
    constructor(sender) {
        this.sender = sender;
        this.maxHeight = 1024;
        this.maxWidth = 1024;
    }

    getExtension(filename) {
        let parts = filename.split('.');
        return parts[parts.length - 1];
    }

    image(file, where = "preview-img", action = "draw") {
        let ext = this.getExtension(file.name);
        if (ext == "gif") {
            this.png(file, where, action);
        } else {
            this.png(file, where, action);
        }
    }

    png(file, where, action) {
        let reader = new FileReader();
        let sender = this.sender;

        let maxHeight = this.maxHeight;
        let maxWidth = this.maxWidth;

        reader.onload = function () {
            let image = new Image();
            image.onload = function () {
                let canvas = document.createElement('canvas');
                let context = canvas.getContext('2d');
                let ratio = Math.min(maxWidth / image.width, maxHeight / image.height);
                canvas.width = image.width * ratio;
                canvas.height = image.height * ratio;
                context.drawImage(image, 0, 0, canvas.width, canvas.height);
                let resized = canvas.toDataURL();
                if (action == "send") {
                    sender.sendText({
                        "image": resized,
                    })
                } else {
                    document.getElementById(where).src = resized;
                }
            };
            image.src = reader.result;
        };
        reader.readAsDataURL(file);
    }

    gif(file, where, action) {
        let reader = new FileReader();

        let maxHeight = this.maxHeight;
        let maxWidth = this.maxWidth;

        reader.onload = function () {
            let image = new Image();
            image.onload = function () {
                // canvas에 이미지 그리기
                var ctx = canvas.getContext("2d");
                ctx.drawImage(img, 0, 0, maxWidth, maxHeight);
                let resized = canvas.toDataURL("image/gif")
                this.sender.sendText({
                    "image": resized,
                })
            };
            image.src = reader.result;
        };
        reader.readAsDataURL(file);
    }

    file(file) {
        var reader = new FileReader();
        var rawData = new ArrayBuffer();
        let sender = this.sender;

        reader.loadend = function () {
        }

        reader.onload = function (e) {
            rawData = e.target.result;

            // ArrayBuffer를 여러 개의 조각으로 분할하여 보내기
            var chunkSize = 1024 * 1024; // 분할 크기 1mb
            var offset = 0;

            sender.sendText({
                'flag': 1,
                "file": file.name,
                "filesize": rawData.byteLength
            })
            while (offset < rawData.byteLength) {
                var chunk = rawData.slice(offset, offset + chunkSize);
                sender.sendBytes(chunk);
                offset += chunkSize;
            }
            sender.sendText({
                'flag': 0,
                "file": file.name,
            })
        }
        reader.readAsArrayBuffer(file);
    }
}