document.addEventListener('DOMContentLoaded', function () {
    var toastElements = document.querySelectorAll('.toast');
    toastElements.forEach(function (toastEl) {
        var toast = new bootstrap.Toast(toastEl, {
            autohide: true,
            delay: 3000 //
        });
        toast.show();
    });
});
