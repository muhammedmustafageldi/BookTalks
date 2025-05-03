document.addEventListener('DOMContentLoaded', searchBook)
let debounceTimer


function searchBook() {
    const input = document.getElementById('search-input')
    const resultContainer = document.getElementById('book-list-container')


    input.addEventListener('input', async function (e) {
        // Reset timeout
        clearTimeout(debounceTimer)

        debounceTimer = setTimeout(async() => {
            const query = e.target.value
            
            // Send query
            const response = await fetch(`/books/search?query=${encodeURIComponent(query)}`)

            if (response.ok) {
                const responseHtml = await response.text()
                resultContainer.innerHTML = responseHtml
            }else {
                resultContainer.innerHTML = "<p class='text-white'>Bir hata oluştu.</p>"
            }
        }, 1000)
    })
}