document.addEventListener("DOMContentLoaded", function() {
    var canvas = document.getElementById('canvas');
    var ctx = canvas.getContext('2d');
    var rect = {};
    var drag = false;
    var imageObj = null;

    function init() {
        document.getElementById('imageLoader').addEventListener('change', handleImage, false);
        canvas.addEventListener('mousedown', mouseDown, false);
        canvas.addEventListener('mouseup', mouseUp, false);
        canvas.addEventListener('mousemove', mouseMove, false);
    }

    function handleImage(e) {
        var reader = new FileReader();
        reader.onload = function(event) {
            imageObj = new Image();
            imageObj.onload = function() {
                canvas.width = imageObj.width;
                canvas.height = imageObj.height;
                ctx.drawImage(imageObj, 0, 0);
            }
            imageObj.src = event.target.result;
        }
        reader.readAsDataURL(e.target.files[0]);     
    }

    function mouseDown(e) {
        rect.startX = e.pageX - canvas.offsetLeft;
        rect.startY = e.pageY - canvas.offsetTop;
        drag = true;
    }

    function mouseUp() {
        drag = false;
        ctx.drawImage(imageObj, 0, 0);
        ctx.strokeRect(rect.startX, rect.startY, rect.w, rect.h);
    }

    function mouseMove(e) {
        if (drag) {
            rect.w = (e.pageX - canvas.offsetLeft) - rect.startX;
            rect.h = (e.pageY - canvas.offsetTop) - rect.startY;
            ctx.clearRect(0, 0, canvas.width, canvas.height);
            ctx.drawImage(imageObj, 0, 0);
            ctx.strokeRect(rect.startX, rect.startY, rect.w, rect.h);
        }
    }

    init();
});
