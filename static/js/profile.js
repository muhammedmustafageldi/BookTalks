addEventListener("DOMContentLoaded", () => {
    setupDeleteFavorite()
})

function setupDeleteFavorite() {
    const favoriteBooksContainer = document.getElementById('favorite-books-container')

    favoriteBooksContainer.addEventListener('click', (event) => {
        const target = event.target
        
        if (target.id === 'delete-favorite'){
            // Clicked button
            const bookId = target.getAttribute('data-book-id')
            
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
                        // call api
                        const response = await fetch(`/api/books/remove_book_from_favorites/?book_id=${bookId}`, {
                            method: 'POST',
                            headers: {'Authorization': `Bearer ${token}`}
                        })

                        if (response.ok) {
                            // Success
                            // Remove deleted item
                            const card = target.closest('.book-card')
                            if (!card) {
                                window.location.reload()
                            } else {
                                // Close dialog and remove item
                                bootstrapModal.hide()
                                card.classList.add('remove-favorite-book-anim')
                                card.addEventListener('animationend', () => {
                                    card.remove()
                                })
                            }

                        } else {
                            // Fail
                            alert("Bir hata oluştu. Lütfen tekrar deneyin.")
                            bootstrapModal.hide()
                        }

                    } catch (error) {
                        console.error(`Error: ${error}`)
                        alert("Bir hata oluştu. Lütfen tekrar deneyin.")
                        bootstrapModal.hide()
                    }

                }
                
            }

        } else {
            // Clicked card
            const card = target.closest('.book-card')
            // Check card
            if (!card) return

            // Get book id from element
            const bookId = card.querySelector('#delete-favorite').getAttribute('data-book-id')
            
            if (!bookId) return

            // Redirect to selected book details
            window.location.href=`/books/book_details/${bookId}`
        }     

    })
}