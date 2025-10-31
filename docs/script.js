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
    
    // Calculate min/max values for scaling
    const nodeValues = coattendanceGraphData.nodes.map(n => n.value || 1);
    const maxNodeValue = Math.max(...nodeValues);
    const minNodeValue = Math.min(...nodeValues);
    const nodeValueRange = maxNodeValue - minNodeValue;
    
    const edgeValues = coattendanceGraphData.edges.map(e => e.value || 1);
    const maxEdgeValue = Math.max(...edgeValues);
    const minEdgeValue = Math.min(...edgeValues);
    const edgeValueRange = maxEdgeValue - minEdgeValue;
    
    // Scale nodes: size based on degree (value)
    // Node size between 10 and 50 pixels
    const scaledNodes = coattendanceGraphData.nodes.map(node => {
        const degree = node.value || 1;
        // Scale size: 10 + (degree - min) / range * 40
        const size = nodeValueRange > 0 
            ? 10 + ((degree - minNodeValue) / nodeValueRange) * 40
            : 25;
        
        // Color based on degree: blue gradient (darker/larger = higher degree)
        // Scale from light blue (0, 150, 255) to dark blue (0, 50, 150)
        const intensity = nodeValueRange > 0 
            ? (degree - minNodeValue) / nodeValueRange
            : 0.5;
        const r = Math.floor(0 + intensity * 0);
        const g = Math.floor(150 - intensity * 100);
        const b = Math.floor(255 - intensity * 105);
        const color = `rgb(${r}, ${g}, ${b})`;
        
        return {
            ...node,
            size: size,
            color: {
                background: color,
                border: '#0366d6',
                highlight: {
                    background: '#0366d6',
                    border: '#002155'
                },
                hover: {
                    background: '#0366d6',
                    border: '#002155'
                }
            },
            font: {
                size: Math.max(10, Math.min(16, size * 0.6)),
                color: '#24292e',
                face: 'Arial',
                bold: degree > maxNodeValue * 0.7
            },
            borderWidth: 2,
            borderWidthSelected: 4
        };
    });
    
    // Scale edges: width based on co-attendance frequency (weight)
    const scaledEdges = coattendanceGraphData.edges.map(edge => {
        const weight = edge.value || 1;
        // Edge width between 1 and 5 pixels
        const width = edgeValueRange > 0
            ? 1 + ((weight - minEdgeValue) / edgeValueRange) * 4
            : 2;
        
        // Color based on weight: lighter gray for frequent, darker for rare
        const opacity = edgeValueRange > 0
            ? 0.3 + ((weight - minEdgeValue) / edgeValueRange) * 0.5
            : 0.5;
        
        return {
            ...edge,
            width: width,
            color: {
                color: `rgba(3, 102, 214, ${opacity})`,
                highlight: '#0366d6',
                hover: '#0366d6'
            },
            smooth: {
                type: 'continuous',
                roundness: 0.5
            },
            selectionWidth: width * 2,
            hoverWidth: width * 1.5
        };
    });
    
    const nodes = new vis.DataSet(scaledNodes);
    const edges = new vis.DataSet(scaledEdges);
    
    const data = {
        nodes: nodes,
        edges: edges
    };
    
    const options = {
        nodes: {
            shape: 'dot',
            font: {
                size: 12,
                color: '#24292e',
                face: 'Arial'
            },
            borderWidth: 2,
            shadow: {
                enabled: true,
                color: 'rgba(0,0,0,0.2)',
                size: 5,
                x: 2,
                y: 2
            }
        },
        edges: {
            smooth: {
                type: 'continuous',
                roundness: 0.5
            },
            arrows: {
                to: {
                    enabled: false
                }
            },
            shadow: {
                enabled: true,
                color: 'rgba(0,0,0,0.1)',
                size: 3
            }
        },
        physics: {
            enabled: true,
            stabilization: {
                iterations: 200,
                updateInterval: 25,
                onlyDynamicEdges: false,
                fit: true
            },
            barnesHut: {
                gravitationalConstant: -2000,
                centralGravity: 0.3,
                springLength: 100,
                springConstant: 0.04,
                damping: 0.09,
                avoidOverlap: 0.5
            }
        },
        interaction: {
            hover: true,
            tooltipDelay: 100,
            zoomView: true,
            dragView: true,
            dragNodes: true,
            selectConnectedEdges: true,
            hideEdgesOnDrag: false,
            hideEdgesOnZoom: false
        },
        layout: {
            improvedLayout: true,
            hierarchical: {
                enabled: false
            }
        }
    };
    
    coattendanceNetwork = new vis.Network(container, data, options);
    
    // Add event listeners for better interactivity
    coattendanceNetwork.on('click', function(params) {
        if (params.nodes.length > 0) {
            const nodeId = params.nodes[0];
            const node = coattendanceGraphData.nodes.find(n => n.id === nodeId);
            if (node) {
                console.log('Selected node:', node);
            }
        }
    });
    
    coattendanceNetwork.on('hoverNode', function(params) {
        container.style.cursor = 'pointer';
    });
    
    coattendanceNetwork.on('blurNode', function(params) {
        container.style.cursor = 'default';
    });
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

