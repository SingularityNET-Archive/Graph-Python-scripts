// Network visualization
let coattendanceNetwork = null;

function initCoattendanceNetwork() {
    if (!coattendanceGraphData || !window.vis) {
        return;
    }
    
    const container = document.getElementById('coattendance-network');
    if (!container) {
        return;
    }
    
    // Destroy existing network if it exists
    if (coattendanceNetwork) {
        coattendanceNetwork.destroy();
    }
    
    const nodes = new vis.DataSet(coattendanceGraphData.nodes);
    const edges = new vis.DataSet(coattendanceGraphData.edges);
    
    const data = {
        nodes: nodes,
        edges: edges
    };
    
    const options = {
        nodes: {
            shape: 'dot',
            size: 16,
            font: {
                size: 12,
                color: '#24292e'
            },
            borderWidth: 2,
            borderColor: '#0366d6'
        },
        edges: {
            width: 2,
            color: {
                color: '#e1e4e8',
                highlight: '#0366d6'
            },
            smooth: {
                type: 'continuous'
            }
        },
        physics: {
            enabled: true,
            stabilization: {
                iterations: 200
            },
            barnesHut: {
                gravitationalConstant: -2000,
                centralGravity: 0.3,
                springLength: 95,
                springConstant: 0.04,
                damping: 0.09
            }
        },
        interaction: {
            hover: true,
            tooltipDelay: 100,
            zoomView: true,
            dragView: true
        }
    };
    
    coattendanceNetwork = new vis.Network(container, data, options);
}

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

    // Initialize network visualization if showing co-attendance tab
    if (tabId === 'coattendance') {
        // Small delay to ensure DOM is ready
        setTimeout(() => {
            initCoattendanceNetwork();
        }, 100);
    }

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

