// Login.js

const loginForm = document.getElementById("login-form")
if (loginForm) {
    loginForm.addEventListener('submit', loginTransaction)
}

async function loginTransaction(event) {
    event.preventDefault()

    const form = event.target
    const formData = new FormData(form)
    
    const payload = new URLSearchParams(formData)

    try {
        const response = await fetch('/auth/token', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded'
            },
            body: payload.toString()
        })

        if (response.ok) {
            const data = await response.json()
            // Delete any cookies available
            logout()
            // Save token to cookie
            document.cookie = `access_token=${data.access_token}; path=/`
            window.location.href = '/books'
        } else {
            // Handle error
            const errorData = await response.json()
            alert(`Error: ${errorData.detail}`);
        }

    } catch (error) {
        console.error('Error: ', error)
        alert('An error occurred. Please try again.')
    }
}