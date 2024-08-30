document.querySelector('.btn').addEventListener('click', function () {
    alert('You are now uploading your file!');
    window.location.href = 'upload_file.html';
});

document.querySelector('.btn-secondary').addEventListener('click', function () {
    alert('Ready to upload another file!');
});

function updateFileName() {
    var fileInput = document.getElementById('file_input');
    var fileNameInput = document.getElementById('file_name');
    var selectedFileMessage = document.getElementById('file-selected-message');
    var selectedFileName = document.getElementById('selected-file-name');
    var removeFileBtn = document.getElementById('remove-file-btn');

    if (fileInput.files.length > 0) {
        var fileName = fileInput.files[0].name;
        fileNameInput.value = fileName;
        selectedFileName.textContent = fileName;
        selectedFileMessage.style.display = 'block';
        removeFileBtn.style.display = 'inline-block';
    } else {
        fileNameInput.value = '';
        selectedFileName.textContent = '';
        selectedFileMessage.style.display = 'none';
        removeFileBtn.style.display = 'none';
    }
}

function removeFile() {
    var fileInput = document.getElementById('file_input');
    var fileNameInput = document.getElementById('file_name');
    var selectedFileMessage = document.getElementById('file-selected-message');
    var removeFileBtn = document.getElementById('remove-file-btn');

    fileInput.value = '';
    fileNameInput.value = '';
    selectedFileMessage.style.display = 'none';
    removeFileBtn.style.display = 'none';
}


