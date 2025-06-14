// Bookdetails.js 
addEventListener("DOMContentLoaded", () => {
    // Clear parentId on load to prevent unintended scroll
    const parentIdInput = document.getElementById("parentIdInput")
    if (parentIdInput) {
        parentIdInput.value = ''
    }

    const commentForm = document.getElementById("leave-a-comment-form")
    if (commentForm) {
        commentForm.addEventListener('submit', leaveAcomment)
    }
    setupReplyListener()
})


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

        // Get parent_id value
        const parentIdInput = document.getElementById("parentIdInput").value
        // Check parentId
        const parentId = parentIdInput ? parseInt(parentIdInput) : null

        // Add comment
        const payload = {
            book_id: bookId,
            content: commentContent,
            parent_id: parentId
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
                // Response data
                const responseData = await response.json()
                // Clear form
                document.getElementById('leave-a-comment-form').reset()
                parentIdInput.value = ""
                document.getElementById("replyInfo").classList.add("d-none")

                // Create new comment partial html ->
                // Send query
                const partialResponse = await fetch(`/comments/render_single_comment/?comment_id=${responseData.id}`)

                if (partialResponse.ok) {
                    const responseHtml = await partialResponse.text()
                    const commentsContainer = document.getElementById("comments-container")
                    
                    // Show create comment anim
                    const tempDiv = document.createElement('div')
                    // Put new comment to html
                    tempDiv.innerHTML += responseHtml.trim()
                    const newComment = tempDiv.querySelector('#comment-item')

                    if (newComment) {
                        commentsContainer.appendChild(newComment)
                        newComment.classList.add('create-comment-animation')
                    }
                    
                } else {
                    // An error occurred. Refresh the page
                    location.reload()
                }

            } else {
                alert('Yorum eklenirken bir sorun oluştu. Lütfen tekrar deneyin.')
            }

        } catch (error) {
            console.error('Error: ', error)
            alert('Bir hata oluştu. Lütfen tekrar deneyin.')
        }
    }



}

function setupReplyListener() {
    // Define required elements ->
    const replyInfoBox = document.getElementById('replyInfo')
    const replyInfoText = document.getElementById('replyingTo')
    const cancelReplyButton = document.getElementById('cancelReply')
    const parentIdInput = document.getElementById('parentIdInput')
    const commentsContainer = document.getElementById('comments-container')

    commentsContainer.addEventListener('click', function (event) {
        const target = event.target

        if (target.classList.contains('reply-button')) {
            // Get values from partial page
            const parentId = target.getAttribute('data-parent-id')
            const username = target.getAttribute('data-parent-username')

            // Fill the hidden parent_id input in the form
            parentIdInput.value = parentId

            // Show reply box ->
            replyInfoBox.classList.remove('d-none')
            replyInfoText.innerText = `"${username}" kişisine yanıt veriyorsunuz`

            // Scroll to form
            const leaveAcommentForm = document.getElementById('leave-a-comment-form')
            if (leaveAcommentForm) {
                leaveAcommentForm.scrollIntoView({ behavior: 'smooth', block: 'center' })
            }
        }
    })

    cancelReplyButton.addEventListener('click', function () {
        // Clear parent id and hide reply box
        parentIdInput.value = ''
        replyInfoText.innerText = ''
        replyInfoBox.classList.add('d-none')
    })
}
