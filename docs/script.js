// Tab switching functionality
function showTab(tabId) {
    // Hide all tab panes
    const tabPanes = document.querySelectorAll('.tab-pane');
    tabPanes.forEach(pane => {
        pane.classList.remove('active');
    });

    // Remove active class from all tab buttons
    const tabButtons = document.querySelectorAll('.tab-button');
    tabButtons.forEach(button => {
        button.classList.remove('active');
    });

    // Show selected tab pane
    const selectedPane = document.getElementById(tabId);
    if (selectedPane) {
        selectedPane.classList.add('active');
    }

    // Add active class to clicked button
    // Map tab IDs to button text patterns
    const tabMap = {
        'summary': 'Summary',
        'coattendance': 'Co-attendance Degree',
        'field-degree': 'Field Degree',
        'path-structure': 'Path Structure',
        'centrality': 'Centrality',
        'clustering': 'Clustering',
        'components': 'Components'
    };
    
    tabButtons.forEach(button => {
        if (button.textContent.trim() === tabMap[tabId]) {
            button.classList.add('active');
        }
    });

    // Update URL hash without scrolling
    if (history.pushState) {
        history.pushState(null, null, '#' + tabId);
    }
}

// Initialize tab from URL hash on page load
window.addEventListener('DOMContentLoaded', function() {
    const hash = window.location.hash.substring(1);
    if (hash) {
        // Check if hash corresponds to a valid tab
        const validTabs = ['summary', 'coattendance', 'field-degree', 'path-structure', 'centrality', 'clustering', 'components'];
        if (validTabs.includes(hash)) {
            showTab(hash);
            return;
        }
    }
    // Default to summary tab
    showTab('summary');
});

// Handle back/forward browser buttons
window.addEventListener('popstate', function() {
    const hash = window.location.hash.substring(1);
    if (hash) {
        const validTabs = ['summary', 'coattendance', 'field-degree', 'path-structure', 'centrality', 'clustering', 'components'];
        if (validTabs.includes(hash)) {
            showTab(hash);
        }
    }
});

