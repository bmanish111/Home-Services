let password1 = document.getElementById('password1')
let password2 = document.getElementById('password2')
passworderror = document.getElementById('password-error')
password2.addEventListener('input', function () {
    if (password1.value !== password2.value) {
        passworderror.classList.add('d-block')
    } else {
        passworderror.classList.remove('d-block')
    }
})