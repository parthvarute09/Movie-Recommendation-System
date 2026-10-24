// main.js

document.addEventListener("DOMContentLoaded", function () {

    const searchInput = document.querySelector("input[name='movie']");
    const suggestionsBox = document.createElement("div");
    suggestionsBox.className = "suggestions-box";
    searchInput.parentNode.appendChild(suggestionsBox);

    let debounceTimeout;

    // Function to fetch search suggestions from Flask API
    const fetchSuggestions = async (query) => {
        if (!query) {
            suggestionsBox.innerHTML = "";
            return;
        }

        try {
            const res = await fetch(`/search?q=${query}`);
            const data = await res.json();

            suggestionsBox.innerHTML = "";
            data.forEach(movie => {
                const div = document.createElement("div");
                div.className = "suggestion-item";
                div.textContent = movie;
                div.addEventListener("click", () => {
                    searchInput.value = movie;
                    suggestionsBox.innerHTML = "";
                });
                suggestionsBox.appendChild(div);
            });
        } catch (err) {
            console.error("Error fetching suggestions:", err);
        }
    };

    // Debounce input to reduce API calls
    searchInput.addEventListener("input", (e) => {
        clearTimeout(debounceTimeout);
        const query = e.target.value;
        debounceTimeout = setTimeout(() => fetchSuggestions(query), 300);
    });

    // Close suggestions if clicking outside
    document.addEventListener("click", (e) => {
        if (!suggestionsBox.contains(e.target) && e.target !== searchInput) {
            suggestionsBox.innerHTML = "";
        }
    });

});