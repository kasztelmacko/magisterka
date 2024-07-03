function onDragStart(event) {
  const itemId = event.currentTarget.id;
  event.dataTransfer.setData('text/plain', itemId);
}

function onDragOver(event) {
  event.preventDefault();
}

function onDrop(event) {
  event.preventDefault();
  
  const itemId = event.dataTransfer.getData('text/plain');
  const draggableElement = document.getElementById(itemId);
  const dropzone = event.target;

  if (!dropzone.hasChildNodes() && dropzone.classList.contains('rectangle')) {
      dropzone.appendChild(draggableElement);
      draggableElement.addEventListener('click', onRemoveFromDropzone);
  }

  event.dataTransfer.clearData();
}

function onRemoveFromDropzone(event) {
  const item = event.currentTarget;
  const itemsContainer = document.getElementById('items-container');
  itemsContainer.appendChild(item);
  item.removeEventListener('click', onRemoveFromDropzone);
}

document.querySelectorAll('.draggable-item').forEach(draggable => {
  draggable.addEventListener('dragstart', onDragStart);
});

document.querySelectorAll('.rectangle').forEach(dropzone => {
  dropzone.addEventListener('dragover', onDragOver);
  dropzone.addEventListener('drop', onDrop);
});


