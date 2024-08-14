document.addEventListener('DOMContentLoaded', function () {
    document.querySelectorAll('input[type="file"]').forEach(function (input) {
        input.addEventListener('change', function () {
            var reader = new FileReader();
            reader.onload = function (e) {
                var previewId = 'image-preview-' + input.name.split('-')[1];
                var previewImg = document.getElementById(previewId);
                if (previewImg) {
                    previewImg.src = e.target.result;
                }
            }
            if (input.files.length) {
                reader.readAsDataURL(input.files[0]);
            }
        });
    });
});