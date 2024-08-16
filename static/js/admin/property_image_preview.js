document.addEventListener('DOMContentLoaded', function () {
    function setupImagePreview() {
        var imageInput = document.querySelector('input[type="file"][name="image"]');
        var previewImg = document.querySelector('img[id^="preview-"]');

        if (imageInput && previewImg) {
            imageInput.addEventListener('change', function () {
                var reader = new FileReader();
                reader.onload = function (e) {
                    previewImg.src = e.target.result;
                    previewImg.style.display = 'block';
                }
                if (this.files.length) {
                    reader.readAsDataURL(this.files[0]);
                }
            });
        }
    }

    setupImagePreview();
});