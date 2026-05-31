document.addEventListener('DOMContentLoaded', () => {
    // --- Theme Toggler ---
    const themeToggleButton = document.querySelector('.theme-toggle-btn');
    const htmlElement = document.documentElement;

    // Function to apply theme
    const applyTheme = (theme) => {
        if (theme === 'dark') {
            htmlElement.classList.add('dark');
        } else {
            htmlElement.classList.remove('dark');
        }
    };

    // Set initial theme on page load
    const savedTheme = localStorage.getItem('theme') || (window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light');
    applyTheme(savedTheme);

    // Handle button click
    if (themeToggleButton) {
        themeToggleButton.addEventListener('click', () => {
            const newTheme = htmlElement.classList.contains('dark') ? 'light' : 'dark';
            applyTheme(newTheme);
            localStorage.setItem('theme', newTheme);
        });
    }

    // --- User Menu Dropdown ---
    const userMenu = document.querySelector('.user-menu');
    if (userMenu) {
        const trigger = userMenu.querySelector('.user-menu-trigger');
        const dropdown = userMenu.querySelector('.user-menu-dropdown');

        if (trigger && dropdown) {
            trigger.addEventListener('click', (event) => {
                event.stopPropagation();
                const isHidden = dropdown.style.display === 'none' || dropdown.style.display === '';
                dropdown.style.display = isHidden ? 'block' : 'none';
            });

            // Close on click outside
            document.addEventListener('click', (event) => {
                if (!userMenu.contains(event.target)) {
                    dropdown.style.display = 'none';
                }
            });
        }
    }
});