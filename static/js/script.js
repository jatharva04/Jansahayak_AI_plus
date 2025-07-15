document.addEventListener('DOMContentLoaded', function() {
    const mainNavbar = document.getElementById('mainNavbar');
    const heroSection = document.getElementById('home');

    // Function to handle the navbar's class on scroll
    function handleNavbarScroll() {
        // If the user has scrolled past a certain point of the hero section
        // (e.g., 100px from its bottom, or more than 80% of its height)
        if (window.scrollY > heroSection.offsetHeight - 100) { 
            mainNavbar.classList.add('scrolled');
        } else {
            mainNavbar.classList.remove('scrolled');
        }
    }

    // Add the scroll event listener
    window.addEventListener('scroll', handleNavbarScroll);

    // Call it once on load to set initial state if page is already scrolled
    handleNavbarScroll(); 
});