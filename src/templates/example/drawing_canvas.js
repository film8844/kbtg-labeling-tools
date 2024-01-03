let canvas = document.getElementById('myCanvas');
let ctx = canvas.getContext('2d');
let image = new Image();
image.src = 'path_to_your_image.jpg'; // Set the path to your image

let scale = 1;
const scaleMultiplier = 0.8;
let startDragOffset = {};
let mouseDown = false;

// Load and display image
image.onload = function() {
    ctx.drawImage(image, 0, 0, canvas.width, canvas.height);
};

function redraw() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    ctx.drawImage(image, 0, 0, image.width * scale, image.height * scale);
}

function zoomIn() {
    scale /= scaleMultiplier;
    redraw();
}

function zoomOut() {
    scale *= scaleMultiplier;
    redraw();
}

function resetView() {
    scale = 1;
    redraw();
}

document.getElementById('zoomInBtn').addEventListener('click', zoomIn);
document.getElementById('zoomOutBtn').addEventListener('click', zoomOut);
document.getElementById('resetBtn').addEventListener('click', resetView);

canvas.addEventListener('wheel', function(event) {
    if (event.deltaY < 0) {
        zoomIn();
    } else {
        zoomOut();
    }
    event.preventDefault();
});

canvas.addEventListener('mousedown', function(e) {
    mouseDown = true;
    startDragOffset.x = e.clientX - canvas.offsetLeft;
    startDragOffset.y = e.clientY - canvas.offsetTop;
});

canvas.addEventListener('mouseup', function(e) {
    mouseDown = false;
});

canvas.addEventListener('mousemove', function(e) {
    if (mouseDown) {
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        ctx.drawImage(image, 0, 0, image.width * scale, image.height * scale);
        ctx.beginPath();
        ctx.rect(startDragOffset.x, startDragOffset.y, e.clientX - canvas.offsetLeft - startDragOffset.x, e.clientY - canvas.offsetTop - startDragOffset.y);
        ctx.strokeStyle = 'red';
        ctx.lineWidth = 2;
        ctx.stroke();
    }
});
