document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('uploadForm');
    const progressBar = document.querySelector('.progress-bar .progress');
    const uploadSpeedElem = document.createElement('div');
    uploadSpeedElem.classList.add('upload-speed');
    progressBar.parentNode.insertBefore(uploadSpeedElem, progressBar.nextSibling);

    form.addEventListener('submit', function(event) {
        event.preventDefault();
        const formData = new FormData(form);
        const xhr = new XMLHttpRequest();
        let startTime, lastLoaded = 0;

        xhr.upload.addEventListener('progress', function(event) {
            if (event.lengthComputable) {
                const percentComplete = (event.loaded / event.total) * 100;
                progressBar.style.width = percentComplete + '%';

                if (!startTime) {
                    startTime = new Date().getTime();
                }

                const currentTime = new Date().getTime();
                const elapsedTime = (currentTime - startTime) / 1000; // Time in seconds
                const bytesUploaded = event.loaded;
                const uploadSpeed = ((bytesUploaded - lastLoaded) / elapsedTime); // Speed in bytes per second

                uploadSpeedElem.textContent = `Speed: ${(uploadSpeed / 1024).toFixed(0)} KB/s`;

                lastLoaded = bytesUploaded;
                startTime = currentTime;
            }
        });

        xhr.onreadystatechange = function() {
            if (xhr.readyState === 4) {
                if (xhr.status === 200) {
                    alert('File uploaded successfully!');
                } else {
                    alert('Error uploading file.');
                }
            }
        };

        xhr.open('POST', form.action);
        xhr.send(formData);
    });
});
