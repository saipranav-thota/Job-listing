document.addEventListener('DOMContentLoaded', function() {
    const bookmarkButton = document.getElementById('bookmarkButton');
    const bookmarkIcon = document.getElementById('bookmarkIcon');

    bookmarkButton.addEventListener('click', function() {
        if (bookmarkIcon.src.includes('bookmark-outline-icon.png')) {
            bookmarkIcon.src = 'bookmark-filled-icon.png';
        } else {
            bookmarkIcon.src = 'bookmark-outline-icon.png';
        }
    });
});
