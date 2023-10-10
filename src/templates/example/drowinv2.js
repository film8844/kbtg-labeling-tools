document.addEventListener('DOMContentLoaded', function () {
    const image = document.getElementById('image');
    const container = document.getElementById('image-container');
    const annotationList = document.getElementById('list');
    const zoomInButton = document.getElementById('zoom-in');
    const zoomOutButton = document.getElementById('zoom-out');
    const zoomLevelSpan = document.getElementById('zoom-level');
    const deleteButton = document.getElementById('delete-button');
    const colorPicker = document.getElementById('color-picker');
    let resizing = false;
    let currentHandle = null;

    let zoomLevel = 100;
    let drawing = false;
    let start_x = 0;
    let start_y = 0;
    let boxes = [];

    let undoStack = [];

    function updateAnnotations() {
        const existingAnnotations = document.querySelectorAll('.annotation');
        existingAnnotations.forEach((annotation) => {
            annotation.remove();
        });

        boxes.forEach((box, index) => createAnnotation(box, index));
    }

    function updateList() {
        annotationList.innerHTML = '';
        boxes.forEach((box, index) => {
            const listItem = document.createElement('li');
            listItem.textContent = `Box ${index + 1}: x=${box.x}, y=${box.y}, width=${box.width}, height=${box.height}`;
            annotationList.appendChild(listItem);
        });
    }

    function adjustZoom(factor) {
        zoomLevel += factor;
        zoomLevel = Math.min(Math.max(zoomLevel, 50), 200);
        image.style.width = `${zoomLevel}%`;
        zoomLevelSpan.textContent = zoomLevel;
        updateAnnotations();
    }

    function createAnnotation(box, index) {
        const annotation = document.createElement('div');
        annotation.className = 'annotation';
        annotation.dataset.index = index;

        annotation.style.borderColor = box.borderColor;
        annotation.style.backgroundColor = box.backgroundColor


        annotation.addEventListener('click', function () {
            annotation.classList.toggle('selected');
        });

        annotation.style.left = `${box.x * zoomLevel / 100}px`;
        annotation.style.top = `${box.y * zoomLevel / 100}px`;
        annotation.style.width = `${box.width * zoomLevel / 100}px`;
        annotation.style.height = `${box.height * zoomLevel / 100}px`;

        ['nw', 'ne', 'sw', 'se','m'].forEach(pos => {
            const handle = document.createElement('div');
            handle.className = `resize-handle ${pos}`;
            handle.style.position = 'absolute';
            if (pos.includes('n')) handle.style.top = '-4px';
            if (pos.includes('s')) handle.style.bottom = '-4px';
            if (pos.includes('w')) handle.style.left = '-4px';
            if (pos.includes('e')) handle.style.right = '-4px';
            if (pos === 'm') {
                handle.style.top = '50%';
                handle.style.left = '50%';
                handle.style.transform = 'translate(-50%, -50%)';
                handle.style.borderRadius = '50%';
            }
            handle.style.width = '8px';
            handle.style.height = '8px';
            handle.style.backgroundColor = box.borderColor;
            annotation.appendChild(handle);
        });

        container.appendChild(annotation);
    }

    image.addEventListener('mousedown', function (event) {
        drawing = true;
        const rect = image.getBoundingClientRect();
        start_x = (event.clientX - rect.left) * 100 / zoomLevel;
        start_y = (event.clientY - rect.top) * 100 / zoomLevel;
    });

    image.addEventListener('mouseup', function (event) {
        if (!drawing) return;
        drawing = false;

        const rect = image.getBoundingClientRect();
        const end_x = (event.clientX - rect.left) * 100 / zoomLevel;
        const end_y = (event.clientY - rect.top) * 100 / zoomLevel;


        const selectedColor = colorPicker.value;
        const borderColor = selectedColor;
        const backgroundColor = 
            selectedColor === 'red' ? 'rgba(255,0,0,0.2)' :
            selectedColor === 'green' ? 'rgba(0,255,0,0.2)' :
            selectedColor === 'blue' ? 'rgba(0,0,255,0.2)' :
            selectedColor === 'yellow' ? 'rgba(255,255,0,0.2)' :
                        'rgba(128,0,128,0.2)'; // Default to purple
        const box = {
            x: Math.min(start_x, end_x),
            y: Math.min(start_y, end_y),
            width: Math.abs(end_x - start_x),
            height: Math.abs(end_y - start_y),
            borderColor:borderColor,
            backgroundColor:backgroundColor
        };
        if (box.height == 0 || box.width == 0) return;
        

        boxes.push(box);
        updateAnnotations();
        updateList();
    });

    zoomInButton.addEventListener('click', function () {
        adjustZoom(10);
    });

    zoomOutButton.addEventListener('click', function () {
        adjustZoom(-10);
    });


    deleteButton.addEventListener('click', function () {
        // Collect all the selected annotations
        const selectedAnnotations = document.querySelectorAll('.annotation.selected');

        // Get their indices
        const indicesToDelete = Array.from(selectedAnnotations).map(annotation => parseInt(annotation.dataset.index, 10));

        // Remove the annotation element from the DOM
        selectedAnnotations.forEach(annotation => {
            annotation.remove();
        });

        // Remove the corresponding boxes
        boxes = boxes.filter((box, index) => !indicesToDelete.includes(index));

        // Update indices and re-render all remaining annotations
        updateAnnotations();
        updateList();
    });

    // Listen for keyboard shortcuts for undo (Ctrl+Z) and redo (Ctrl+Shift+Z)
    document.addEventListener('keydown', function (event) {

        if (event.key === 'Backspace') {
            // Perform deletion here
            const selectedAnnotations = document.querySelectorAll('.annotation.selected');

            // Get their indices
            const indicesToDelete = Array.from(selectedAnnotations).map(annotation => parseInt(annotation.dataset.index, 10));

            // Remove the annotation element from the DOM
            selectedAnnotations.forEach(annotation => {
                annotation.remove();
            });

            // Remove the corresponding boxes
            boxes = boxes.filter((box, index) => !indicesToDelete.includes(index));

            // Update indices and re-render all remaining annotations
            updateAnnotations();
            updateList();
        }


        // Check if Ctrl+Z is pressed
        if (event.ctrlKey && event.key === 'z') {
            if (boxes.length > 0) {
                // Pop the last box and store it in the undo stack
                const lastBox = boxes.pop();
                undoStack.push(lastBox);

                // Update annotations and list
                updateAnnotations();
                updateList();
            }
        }
        // Implement Ctrl+Shift+Z for redo
        else if (event.ctrlKey && event.shiftKey && event.key === 'Z') {
            if (undoStack.length > 0) {
                // Pop the last undone box and put it back in boxes
                const lastUndoneBox = undoStack.pop();
                boxes.push(lastUndoneBox);

                // Update annotations and list
                updateAnnotations();
                updateList();
            }
        }
    });
    container.addEventListener('mousedown', function (event) {
        const handle = event.target.closest('.resize-handle');
        if (handle) {
            resizing = true;
            currentHandle = handle;
            console.log(currentHandle);
        }
    });
    
    document.addEventListener('mouseup', function () {
        resizing = false;
        currentHandle = null;
    });

    container.addEventListener('mousemove', function (event) {
        if (!resizing || !currentHandle) return;
        const rect = image.getBoundingClientRect();
        const x = (event.clientX - rect.left) * 100 / zoomLevel;
        const y = (event.clientY - rect.top) * 100 / zoomLevel;
        const box = boxes[parseInt(currentHandle.parentElement.dataset.index)];
        const canses = currentHandle.className.split(' ')[1]
    
        switch (canses) {
            case 'nw':
                box.width += box.x - x;
                box.height += box.y - y;
                box.x = x;
                box.y = y;
                break;
            case 'ne':
                box.width = x - box.x;
                box.height += box.y - y;
                box.y = y;
                break;
            case 'sw':
                box.width += box.x - x;
                box.height = y - box.y;
                box.x = x;
                break;
            case 'se':
                box.width = x - box.x;
                box.height = y - box.y;
                break;
            case 'm':
                const deltaX = x - (box.x + box.width/2);
                const deltaY = y - (box.y + box.height/2);
                box.x += deltaX;
                box.y += deltaY;
        }
    
        updateAnnotations();
        updateList();
    });
    

});
