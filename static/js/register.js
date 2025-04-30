// Register.js
const registerForm = document.getElementById("register-form")
if (registerForm) {
    registerForm.addEventListener('submit', registerTransaction)
}

async function registerTransaction(event) {
    event.preventDefault()
    
    const form = event.target
    const formData = new FormData(form)
    const data = Object.fromEntries(formData.entries())

    if (data.password !== data["verify-password"]) {
        alert("Passwords do not match")
        return
    }

    const payload = {
        email: data.email,
        username: data.username,
        password: data.password
    }

    try {
        const response = await fetch('/auth/create_user', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(payload)
        })

        if (response.ok) {
            console.log("Successful")
            // Redirect to login page
            window.location.href = '/auth/login-page'
        } else {
            // Eğer Request validation dan geçmezse buraya giriyor fakat kullanıcı bir şey görmüyor!
            console.log("Fail")
        }

    } catch (error) {
        console.error('Error: ', error)
        alert('An error occurred. Please try again.');
    }
}