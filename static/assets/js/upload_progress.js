document.addEventListener('DOMContentLoaded', function() {
    const form = document.querySelector('form');
    const progressBar = document.createElement('div');
    progressBar.classList.add('progress-bar');
    const progress = document.createElement('div');
    progress.classList.add('progress');
    progressBar.appendChild(progress);
    form.appendChild(progressBar);

    form.addEventListener('submit', function(event) {
        const formData = new FormData(form);
        const xhr = new XMLHttpRequest();

        xhr.upload.addEventListener('progress', function(event) {
            if (event.lengthComputable) {
                const percentComplete = (event.loaded / event.total) * 100;
                progress.style.width = percentComplete + '%';
            }
        });

        xhr.open('POST', form.action);
        xhr.send(formData);

        event.preventDefault();
    });
});
