
// document.addEventListener('DOMContentLoaded', function() {
//     fetch(jobsUrl)
//         .then(response => response.json())
//         .then(data => {
//             const jobListings = document.getElementById('jobListings');
            
//             data.forEach(job => {
//                 const jobElement = document.createElement('div');
//                 jobElement.className = 'job';
                
//                 jobElement.innerHTML = `
//                     <div class='compay-details'>
//                         <div class="position">
//                             <p>${job.position}</p>
//                         </div>
//                         <div class="company">
//                             <p>${job.company}</p>
//                         </div>
//                     </div>
//                     <div class="job-details-details">
//                         ${job.details.map(detail => `<span>${detail}</span>`).join('')}
//                     </div>
//                     <div class="location">
//                         <p>${job.location}</p>
//                     </div>
//                     <div class="time">
//                         <p>${job.time}</p>
//                     </div>
//                     <div class="bookmark-container">
//                         <button class="bookmark">
//                             <img src="static/bookmark-outline-icon.png" alt="Bookmark" class="bookmark-icon">
//                         </button>
//                     </div>
//                 `;
                
//                 jobListings.appendChild(jobElement);
//             });

//             document.querySelectorAll('.bookmark').forEach(button => {
//                 button.addEventListener('click', function() {
//                     const icon = this.querySelector('.bookmark-icon');
//                     if (icon.src.includes('bookmark-outline-icon.png')) {
//                         icon.src = 'static/bookmark-filled-icon.png';
//                     } else {
//                         icon.src = 'static/bookmark-outline-icon.png';
//                     }
//                 });
//             });
//         })
//         .catch(error => console.error('Error fetching job data:', error));
// });



$(document).ready(function() {
    let debounce;
    let showSuggestions = true; // Start with suggestions enabled

    $('.search-input').on('keydown', function(e) {
        // Check if the Escape key is pressed
        if (e.key === "Escape") {
            $('.results').empty(); // Clear suggestions
            showSuggestions = false; // Disable showing suggestions
            return; // Exit the function
        }

        // Allow showing suggestions again only if it's a character key
        if (e.key.length === 1 || e.key === "Backspace") { // Consider character keys and backspace
            clearTimeout(debounce);
            debounce = setTimeout(() => {
                const query = $('.search-input').val().trim();
                
                // Fetch suggestions only if there is a query
                if (query.length > 0) {
                    showSuggestions = true; // Enable showing suggestions
                    getAutoComplete(query);
                } else {
                    $('.results').empty(); // Clear suggestions if input is empty
                    showSuggestions = false; // Update flag since suggestions are hidden
                }
            }, 300);
        }
    });
});

// Search box function
function getAutoComplete(query) {
    fetch(`http://127.0.0.1:5000/search?q=${encodeURIComponent(query)}`)
        .then((resp) => resp.json())
        .then((data) => {
            $('.results').empty();
            if (data.length > 0) { // Only show if suggestions are enabled
                for (let i = 0; i < data.length; i++) {
                    $('.results').append(`<li>${data[i]}</li>`);
                }
            }
        });
}

// Optional: Add click event to the suggestions
$(document).on('click', '.results li', function() {
    $('.search-input').val($(this).text()); // Populate input with selected suggestion
    $('.results').empty(); // Clear suggestions
    postQueryToBackend(selectedQuery);
});

function postQueryToBackend(query) {
    // If query is empty, send a special request to get all jobs
    if (query.trim() === '') {
        console.log('Search box is empty, fetching all jobs...');
        fetchAllJobs();
    } else {
        // Post the selected query to the backend
        fetch(`http://127.0.0.1:5000/post_query`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ query: query }) // Send the selected query as JSON
        })
        .then((response) => response.json())
        .then((data) => {
            console.log('Query posted to backend:', data);
            // Handle response or update UI as needed
        })
        .catch((error) => {
            console.error('Error posting query to backend:', error);
        });
    }
}

// Function to fetch all jobs when the search box is empty
function fetchAllJobs() {
    fetch(`http://127.0.0.1:5000/home`)
    .then((response) => response.text())
    .then((html) => {
        $('#jobListings').html(html); // Update the job listings with the full list of jobs
    })
    .catch((error) => {
        console.error('Error fetching all jobs:', error);
    });
}