document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('openFormBtn').addEventListener('click', function() {
        document.getElementById('popupForm').style.display = 'block';
    });

    // Close the form when the user clicks outside of it
    window.addEventListener('click', function(event) {
        var form = document.getElementById('popupForm');
        if (event.target != form && !form.contains(event.target)) {
            form.style.display = 'none';
        }
    });
});
