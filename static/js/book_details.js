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
    setupDeleteListeners()
    setupFavoriteTransaction()
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
        return
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
                        // Add default properties
                        newComment.style.opacity = '0'
                        newComment.style.transform = 'scale(0)'

                        commentsContainer.appendChild(newComment)

                        setTimeout(() => {
                            newComment.classList.add('create-comment-animation')
                        }, 50)  
                    }

                    // "no-comment-container" hide if there is
                    const noCommentBox = document.querySelector('.no-comment-container')
                    if (noCommentBox) {
                        noCommentBox.style.display = 'none'
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

function setupDeleteListeners() {
    const commentsContainer = document.getElementById('comments-container')

    commentsContainer.addEventListener('click', async function (event) {
        const target = event.target

        const deleteButton = target.closest('.delete-comment-btn')
        if (deleteButton) {
            const comment_id = deleteButton.getAttribute('data-comment-id')

            // Show modal
            const deleteModal = document.getElementById('deleteConfirmModal')
            const bootstrapModal = new bootstrap.Modal(deleteModal)
            bootstrapModal.show()

            document.getElementById('confirmDeleteButton').onclick = async function () {

                // Get and check token 
                const token = getCookie('access_token')
                if (!token) {
                    logout()
                    return
                } else {
                    try {
                        // Call api
                        const response = await fetch(`/api/comments/delete/?comment_id=${comment_id}`, {
                            method: 'DELETE',
                            headers: {
                                'Authorization': `Bearer ${token}`
                            }
                        })
                        if (response) {
                            // Remove deleted item
                            const commentItem = deleteButton.closest('.comment-item')
                            if (commentItem) {
                                commentItem.classList.add('remove-comment-anim')
                                commentItem.addEventListener('animationend', () => {
                                    commentItem.remove()
                                })
                            }
                            bootstrapModal.hide()
                        } else {
                            alert('Silme işlemi başarısız oldu.')
                        }

                    } catch (error) {
                        console.error('Error: ', error)
                        alert('Bir hata oluştu. Lütfen tekrar deneyin.')
                    }
                }
            }
        }
    })

}

function setupFavoriteTransaction () {
    const favoriteButton = document.getElementById('favoriteButton')
    const bookDetailDiv = document.getElementById('bookDetails')
    const book_id = bookDetailDiv.getAttribute('data-book-id')

    favoriteButton.addEventListener('click', async () => {
        // Get token 
        const token = getCookie('access_token')
        if (!token) {
            logout()
            return
        }

        // Check book is favorite
        const isFavorite = favoriteButton.getAttribute('data-favorite') === '1'

        try {
            let response 

            if (isFavorite) {
                // Book is favorite
                // Remove book from favorite list.
                response = await fetch(`/api/books/remove_book_from_favorites/?book_id=${book_id}`, {
                    method: 'POST',
                    headers: {'Authorization': `Bearer ${token}`}
                })
            } else {
                // Book is not favorite
                // Add book to favorite list
                response = await fetch(`/api/books/add_book_to_favorites/?book_id=${book_id}`, {
                    method: 'POST',
                    headers: {'Authorization': `Bearer ${token}`}
                })
            }

            if (response.ok) {
                if (isFavorite) {
                    // Removed from favorite
                    favoriteButton.setAttribute('data-favorite', '0')
                    // Change icon
                    const buttonIcon = favoriteButton.querySelector('i')
                    buttonIcon.classList.remove('text-warning')
                    buttonIcon.classList.replace('bi-star-fill', 'bi-star')
                    favoriteButton.querySelector('span').innerText = 'Favoriye Ekle'
                } else {
                    // Added to favorite
                    favoriteButton.setAttribute('data-favorite', '1')
                    //Change icon
                    const buttonIcon = favoriteButton.querySelector('i')
                    buttonIcon.classList.add('text-warning')
                    buttonIcon.classList.replace('bi-star', 'bi-star-fill')
                    favoriteButton.querySelector('span').innerText = 'Favorilerde'
                }

            } else {
                alert("İşlem sırasında bir hata oluştu.")
            }

        } catch (error) {
            console.error(`Error: ${error}`)
            alert('Favori işlemi sırasında bir hata oluştu. Lütfen tekrar deneyin.')
        }
    })
}