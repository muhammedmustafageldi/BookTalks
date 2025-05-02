document.addEventListener('DOMContentLoaded', searchBook)
let debounceTimer

function searchBook() {
    const input = document.getElementById('search-input')
    const resultContainer = document.getElementById('book-list')

    input.addEventListener('input', async function (e) {
        // Reset timeout
        clearTimeout(debounceTimer)

        debounceTimer = setTimeout(async () => {
            const query = e.target.value
            const authorId = window.location.pathname.split('/').pop()
    
            const response = await fetch(`/authors/author_details/${authorId}/search?query=${encodeURIComponent(query)}`);
    
            if (response.ok) {
                const responseHtml = await response.text()
                resultContainer.innerHTML = responseHtml
            } else {
                resultContainer.innerHTML = "<p class='text-white'>Bir hata oluştu.</p>";
            }
        }, 1000)
    })

}