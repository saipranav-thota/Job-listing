
document.addEventListener('DOMContentLoaded', function() {
    fetch(jobsUrl)
        .then(response => response.json())
        .then(data => {
            const jobListings = document.getElementById('jobListings');
            
            data.forEach(job => {
                const jobElement = document.createElement('div');
                jobElement.className = 'job';
                
                jobElement.innerHTML = `
                    <div class='compay-details'>
                        <div class="position">
                            <p>${job.position}</p>
                        </div>
                        <div class="company">
                            <p>${job.company}</p>
                        </div>
                    </div>
                    <div class="job-details-details">
                        ${job.details.map(detail => `<span>${detail}</span>`).join('')}
                    </div>
                    <div class="location">
                        <p>${job.location}</p>
                    </div>
                    <div class="time">
                        <p>${job.time}</p>
                    </div>
                    <div class="bookmark-container">
                        <button class="bookmark">
                            <img src="static/bookmark-outline-icon.png" alt="Bookmark" class="bookmark-icon">
                        </button>
                    </div>
                `;
                
                jobListings.appendChild(jobElement);
            });

            document.querySelectorAll('.bookmark').forEach(button => {
                button.addEventListener('click', function() {
                    const icon = this.querySelector('.bookmark-icon');
                    if (icon.src.includes('bookmark-outline-icon.png')) {
                        icon.src = 'static/bookmark-filled-icon.png';
                    } else {
                        icon.src = 'static/bookmark-outline-icon.png';
                    }
                });
            });
        })
        .catch(error => console.error('Error fetching job data:', error));
});

