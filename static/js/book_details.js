// Bookdetails.js 
const commentForm = document.getElementById("leave-a-comment-form")
if (commentForm) {
    commentForm.addEventListener('submit', leaveAcomment)
}


async function leaveAcomment(event) {
    event.preventDefault()

    const bookDetailsDiv = document.getElementById("bookDetails")
    const bookId = bookDetailsDiv.dataset.bookId

    const commentContent = document.getElementById("commentText").value.trim()
    if (!commentContent) {
        alert("Lütfen bir yorum girin.")
        return 
    }

    // Get token. Func from base.js
    const token = getCookie('access_token')
    if (!token) {
        // Token not found. Redirect to login screen
        logout()
    } else {
        // Add comment
        const payload = {
            book_id: bookId,
            content: commentContent,
            parent_id: null
        }

        try {
            const response = await fetch('/api/comments/add', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            },
            body: JSON.stringify(payload)
            })

            if (response.ok) {
                // Clear form
                document.getElementById('leave-a-comment-form').reset()
                // Create new comment partial html ->

            } else {
                alert('Yorum eklenirken bir sorun oluştu. Lütfen tekrar deneyin.')
            }

        } catch (error) {
            console.error('Error: ', error)
            alert('Bir hata oluştu. Lütfen tekrar deneyin.')
        }
    }

    

}