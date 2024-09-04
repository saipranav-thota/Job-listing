document.addEventListener('DOMContentLoaded', function() {
    fetch('jobs.json')
        .then(response => response.json())
        .then(data => {
            const jobListings = document.getElementById('jobListings');
            
            data.forEach(job => {
                const jobElement = document.createElement('div');
                jobElement.className = 'job';
                
                jobElement.innerHTML = `
                    <div class="job-details">
                        <div class="job-details-pos">
                            <div class="position">
                                <p>${job.position}</p>
                            </div>
                            <div class="job-company">
                                <p>${job.company}</p>
                            </div>
                        </div>
                        <div class="job-details-details">
                            ${job.details.map(detail => `<span>${detail}</span>`).join('')}
                        </div>
                        <div class="job-details-location">
                            <p>${job.location}</p>
                        </div>
                        <div class="job-timing">
                            <p>${job.time}</p>
                        </div>
                        <div class="bookmark-container">
                            <button class="bookmark">
                                <img src="bookmark-outline-icon.png" alt="Bookmark" class="bookmark-icon" id="bookmarkIcon">
                            </button>
                        </div>
                    </div>
                `;
                
                jobListings.appendChild(jobElement);
            });

            // Add toggle functionality for bookmarks
            document.querySelectorAll('.bookmark').forEach(button => {
                button.addEventListener('click', function() {
                    const icon = this.querySelector('.bookmark-icon');
                    if (icon.src.includes('bookmark-outline-icon.png')) {
                        icon.src = 'bookmark-filled-icon.png';
                    } else {
                        icon.src = 'bookmark-outline-icon.png';
                    }
                });
            });
        })
        .catch(error => console.error('Error fetching job data:', error));
});