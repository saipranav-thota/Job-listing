$(document).ready(function() {
    let debounce;
    let showSuggestions = true; // Start with suggestions enabled

    // Search functionality
    $('.search-input').on('keydown', function(e) {
        if (e.key === "Escape") {
            $('.results').empty(); // Clear suggestions
            showSuggestions = false; // Disable showing suggestions
            return; // Exit the function
        }

        if (e.key.length === 1 || e.key === "Backspace") {
            clearTimeout(debounce);
            debounce = setTimeout(() => {
                const query = $('.search-input').val().trim();

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

    // Fetch autocomplete suggestions
    function getAutoComplete(query) {
        fetch(`http://127.0.0.1:5000/search?q=${encodeURIComponent(query)}`)
            .then((resp) => resp.json())
            .then((data) => {
                $('.results').empty();
                if (data.length > 0 && showSuggestions) {
                    for (let i = 0; i < data.length; i++) {
                        $('.results').append(`<li>${data[i]}</li>`);
                    }
                }
            });
    }

    // Click event for suggestion selection
    $(document).on('click', '.results li', function() {
        $('.search-input').val($(this).text()); // Populate input with selected suggestion
        $('.results').empty(); // Clear suggestions
        postQueryToBackend($(this).text());
    });

    // Function to post the query to the backend
    function postQueryToBackend(query) {
        if (query.trim() === '') {
            console.log('Search box is empty, fetching all jobs...');
            fetchAllJobs();
        } else {
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
            })
            .catch((error) => {
                console.error('Error posting query to backend:', error);
            });
        }
    }

    //Function to fetch all jobs
    function fetchAllJobs() {
        fetch(`http://127.0.0.1:5000/home`)
        .then((response) => response.text())
        .then((html) => {
            $('#jobListings').html(html); // Update job listings
        })
        .catch((error) => {
            console.error('Error fetching all jobs:', error);
        });
    }

    $('.dropdown-content').each(function() {
        // Inject the initial SVG icon (chevron-down)
        $(this).html(`
            <svg xmlns="http://www.w3.org/2000/svg" width="27" height="27" fill="currentColor" class="bi bi-chevron-up" viewBox="0 0 16 16">
                <path fill-rule="evenodd" d="M7.646 4.646a.5.5 0 0 1 .708 0l6 6a.5.5 0 0 1-.708.708L8 5.707l-5.646 5.647a.5.5 0 0 1-.708-.708z"/>
            </svg>
        `);
    });

    // Collapsible functionality
    $('.dropdown-content').click(function() {
        $(this).toggleClass("active");
        $(this).next('.Dropdown-details').slideToggle(); // Use slideToggle for smooth animation

        let svgIcon = $(this).find('svg');
        if ($(this).hasClass("active")) {
            svgIcon.html(`
                <path fill-rule="evenodd" d="M1.646 4.646a.5.5 0 0 1 .708 0L8 10.293l5.646-5.647a.5.5 0 0 1 .708.708l-6 6a.5.5 0 0 1-.708 0l-6-6a.5.5 0 0 1 0-.708"/>
              `);
        } else {
            svgIcon.html(`
                <path fill-rule="evenodd" d="M7.646 4.646a.5.5 0 0 1 .708 0l6 6a.5.5 0 0 1-.708.708L8 5.707l-5.646 5.647a.5.5 0 0 1-.708-.708z"/>
            `);
        }
    });

    const slider = document.querySelector('.slider');
    const sliderBalloon = document.querySelector('.slider-balloon p');
    const limit2 = document.querySelector(".limit-2");

    const percentage = 100;
    slider.style.background = `linear-gradient(to right, #000 ${percentage}%, #ddd ${percentage}%)`;
    sliderBalloon.textContent = "Any";
    limit2.textContent = "Any";     
    sliderBalloon.parentElement.style.left = `81%`;


    function sliderActive() {
      const value = slider.value;
      const min = slider.min;
      const max = slider.max;
      const percentage = ((value - min) / (max - min)) * 100;

      // Set the filled portion to black
      slider.style.background = `linear-gradient(to right, #000 ${percentage}%, #ddd ${percentage}%)`;

      // Update the displayed value in the balloon
      sliderBalloon.textContent = value;
      limit2.textContent = "30 Yrs";

      // Position the balloon above the thumb
      const thumbWidth = 25; // Width of the thumb
      const sliderWidth = slider.offsetWidth;
      const balloonWidth = sliderBalloon.offsetWidth;
    
      // Calculate the position of the balloon
      const leftPosition = (percentage * (sliderWidth - thumbWidth) / 100) + (thumbWidth / 2) - (balloonWidth / 2);

      // Apply calculated left position
      sliderBalloon.parentElement.style.left = `${leftPosition-10}px`;
    }

    // Update on input change
    slider.addEventListener('input', sliderActive);

    // Show the current value on thumb click
    slider.addEventListener('click', sliderActive);







    document.querySelector('.apply-filters').addEventListener('submit', function(event) {
        event.preventDefault(); // Prevent the default form submission
    
        // Create a URLSearchParams object to store query parameters
        const queryParams = new URLSearchParams();
    
        // 1. Collect checked checkboxes
        const checkboxes = this.querySelectorAll('input[type="checkbox"]:checked');
        checkboxes.forEach(checkbox => {
            const sectionName = checkbox.closest('.Dropdown-details').previousElementSibling.previousElementSibling.textContent.trim(); // Get the section heading like 'Employment', 'Work Mode', etc.
            const labelText = checkbox.closest('label').textContent.trim(); // Get the label text like 'Fulltime', 'Remote', etc.
            
            // Add the section name and value to the query string (multiple selections under the same filter will use the same key)
            queryParams.append(sectionName, labelText);
        });
    
        // 2. Collect the range slider value
        const slider = this.querySelector('input[type="range"]');
        const experience = slider.value; // Get the slider value
        if(sliderBalloon.textContent == "Any"){
            queryParams.append('Experience', -1);  
        } 
        else{
            queryParams.append('Experience', experience); // Add 'Experience' slider value
        }
        // 3. Redirect to the backend with query parameters
        const queryString = queryParams.toString(); // Convert to query string format
        window.location.href = `${this.action}?${queryString}`; // Redirect to the backend URL with query string
    });
});

