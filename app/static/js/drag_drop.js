document.addEventListener('DOMContentLoaded', (event) => {
  document.querySelectorAll('.draggable-item').forEach(draggable => {
    draggable.addEventListener('dragstart', onDragStart);
  });

  document.querySelectorAll('.rectangle').forEach(dropzone => {
    dropzone.addEventListener('dragover', onDragOver);
    dropzone.addEventListener('drop', onDrop);
  });
});

function onDragStart(event) {
  event.dataTransfer.setData('text/plain', event.target.id);
}

function onDragOver(event) {
  event.preventDefault();
}

function onDrop(event) {
  event.preventDefault();
  
  const itemId = event.dataTransfer.getData('text/plain');
  const draggableElement = document.getElementById(itemId);
  const dropzone = event.currentTarget;

  if (!dropzone.querySelector('.draggable-item') && dropzone.classList.contains('rectangle')) {
    dropzone.appendChild(draggableElement);
    draggableElement.addEventListener('click', onRemoveFromDropzone);

    // Update the hidden input field with the item name
    const itemName = draggableElement.querySelector('h5').textContent.trim();
    const hiddenInput = dropzone.querySelector('input[type="hidden"]');
    hiddenInput.value = itemName;
  }

  event.dataTransfer.clearData();
}

function onRemoveFromDropzone(event) {
  const item = event.currentTarget;
  const itemsContainer = document.getElementById('items-container');
  
  // Check if it's a left-click without modifier keys (Ctrl, Shift, Alt, etc.)
  if (event.button === 0 && !event.ctrlKey && !event.shiftKey && !event.altKey && !event.metaKey) {
    itemsContainer.appendChild(item);
    item.removeEventListener('click', onRemoveFromDropzone);

    // Clear the hidden input field in the dropzone
    const dropzone = item.parentElement;
    const hiddenInput = dropzone.querySelector('input[type="hidden"]');
    hiddenInput.value = '';
  }
}

document.addEventListener('DOMContentLoaded', (event) => {
  const form = document.getElementById('dropzone-form');
  form.addEventListener('submit', function(event) {
    // Prevent form submission initially
    event.preventDefault();
    
    // Validate each hidden input field
    const rect1Input = document.getElementById('rect1_name');
    const rect2Input = document.getElementById('rect2_name');
    const rect3Input = document.getElementById('rect3_name');
    const rect4Input = document.getElementById('rect4_name');
    const rect5Input = document.getElementById('rect5_name');
    
    if (validateInput(rect1Input) && 
        validateInput(rect2Input) && 
        validateInput(rect3Input) && 
        validateInput(rect4Input) && 
        validateInput(rect5Input)) {
      form.submit();
    } else {
      alert('Please fill in all fields before submitting.');
    }
  });

  function validateInput(input) {
    return input.value.trim() !== '';
  }
});

