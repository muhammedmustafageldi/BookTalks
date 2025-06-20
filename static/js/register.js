// Register.js
addEventListener('DOMContentLoaded', () => {
    const registerForm = document.getElementById("register-form")
    if (registerForm) {
        registerForm.addEventListener('submit', registerTransaction)
    }

    setupImgPreview()
})

function setupImgPreview() {
    const imageInput = document.getElementById('profileImageInput')
    const imagePreview = document.getElementById('profileImagePreview')

    if (imageInput && imagePreview) {
        imageInput.addEventListener('change', function(event) {
            const file = event.target.files[0]
            if (file) {
                const reader = new FileReader()
                reader.onload = function(e) {
                    imagePreview.src = e.target.result
                }
                reader.readAsDataURL(file)
            }
        })
    }
}

async function registerTransaction(event) {
    event.preventDefault()
    
    const form = event.target
    const formData = new FormData(form)

    const password = formData.get("password")
    const verifyPassword = document.getElementById('verify-password').value

    if (password !== verifyPassword) {
        alert("Parolalar eşleşmiyor.")
        return
    }

    try {
        const response = await fetch('/auth/create_user', {
            method: 'POST',
            body: formData
        })

        if (response.ok) {
            console.log("Successful")
            // Redirect to login page
            window.location.href = '/auth/login-page'
        } else {
            console.log("Fail")
            alert("Geçersiz form verileri. Lütfen kontrol edip tekrar deneyin.")
        }

    } catch (error) {
        console.error('Error: ', error)
        alert('Bir hata oluştu. Lütfen tekrar deneyin.')
    }
}