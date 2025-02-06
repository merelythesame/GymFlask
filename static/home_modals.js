document.addEventListener('DOMContentLoaded', function () {
    let depositBtn = document.getElementById('btn_deposit');
    let changePasswordBtn = document.getElementById('btn_changePassword');

    depositBtn.addEventListener('click', function () {
        let depositModal = new bootstrap.Modal(document.getElementById('depositModal'));
        depositModal.show();
    });

    changePasswordBtn.addEventListener('click', function () {
        let changePasswordModal = new bootstrap.Modal(document.getElementById('changePasswordModal'));
        changePasswordModal.show();
    });
});
