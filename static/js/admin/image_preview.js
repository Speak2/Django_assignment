document.addEventListener('DOMContentLoaded', function () {
    function setupImagePreviews() {
        document.querySelectorAll('input[type="file"]').forEach(function (input) {
            input.addEventListener('change', function () {
                var reader = new FileReader();
                reader.onload = function (e) {
                    var row = input.closest('tr');
                    var previewImg = row.querySelector('.image-preview');
                    if (previewImg) {
                        previewImg.src = e.target.result;
                    }
                }
                if (input.files.length) {
                    reader.readAsDataURL(input.files[0]);
                }
            });
        });
    }

    // Initial setup
    setupImagePreviews();

    // Setup for dynamically added rows
    if (typeof django !== 'undefined' && django.jQuery) {
        django.jQuery(document).on('formset:added', function(event, $row, formsetName) {
            setupImagePreviews();
        });
    }
});