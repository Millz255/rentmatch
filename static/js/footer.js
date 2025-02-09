document.addEventListener("DOMContentLoaded", function() {
    function adjustFooter() {
        var body = document.body;
        var html = document.documentElement;
        var footer = document.querySelector('footer');
        var wrapper = document.querySelector('.wrapper');

        var bodyHeight = Math.max(body.scrollHeight, body.offsetHeight,
            html.clientHeight, html.scrollHeight, html.offsetHeight);

        var viewportHeight = window.innerHeight;

        if (bodyHeight < viewportHeight) {
            wrapper.style.minHeight = viewportHeight + 'px';
        } else {
            wrapper.style.minHeight = 'auto';
        }
    }

    // Initial adjustment
    adjustFooter();

    // Adjust on window resize
    window.addEventListener('resize', adjustFooter);
});


document.addEventListener("DOMContentLoaded", function() {
    console.log('Footer JS loaded and running');
    function adjustFooter() {
        var body = document.body;
        var html = document.documentElement;
        var footer = document.querySelector('footer');
        var wrapper = document.querySelector('.wrapper');

        var bodyHeight = Math.max(body.scrollHeight, body.offsetHeight,
            html.clientHeight, html.scrollHeight, html.offsetHeight);

        var viewportHeight = window.innerHeight;

        if (bodyHeight < viewportHeight) {
            wrapper.style.minHeight = viewportHeight + 'px';
        } else {
            wrapper.style.minHeight = 'auto';
        }
    }

    // Initial adjustment
    adjustFooter();

    // Adjust on window resize
    window.addEventListener('resize', adjustFooter);
});
