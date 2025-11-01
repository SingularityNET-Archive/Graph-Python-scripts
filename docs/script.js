// Network visualization
let coattendanceNetwork = null;
let initRetryCount = 0;
const MAX_INIT_RETRIES = 10;

function initCoattendanceNetwork() {
    try {
        // Check prerequisites - wait for vis library if needed
        if (!window.vis || !window.vis.Network || !window.vis.DataSet) {
            if (initRetryCount < MAX_INIT_RETRIES) {
                initRetryCount++;
                console.warn(`vis-network library not loaded yet, retrying (${initRetryCount}/${MAX_INIT_RETRIES})...`);
                setTimeout(() => {
                    initCoattendanceNetwork();
                }, 100);
            } else {
                console.error('vis-network library failed to load after multiple retries');
            }
            return;
        }
        
        initRetryCount = 0; // Reset retry count on success
        
        if (!coattendanceGraphData) {
            console.error('coattendanceGraphData not found');
            return;
        }
        
        if (!coattendanceGraphData.nodes || !Array.isArray(coattendanceGraphData.nodes) || coattendanceGraphData.nodes.length === 0) {
            console.error('No nodes data available');
            return;
        }
        
        const container = document.getElementById('coattendance-network');
        if (!container) {
            console.error('Container element not found');
            return;
        }
        
        // Check if container is visible (not hidden by tab system)
        const tabPane = container.closest('.tab-pane');
        if (tabPane && !tabPane.classList.contains('active')) {
            console.log('Container not visible, will initialize when tab is shown');
            return;
        }
        
        // Destroy existing network if it exists
        if (coattendanceNetwork) {
            coattendanceNetwork.destroy();
            coattendanceNetwork = null;
        }
        
        // Calculate min/max values for scaling
        const nodeValues = coattendanceGraphData.nodes.map(n => n.value || 1);
        if (nodeValues.length === 0) {
            console.error('No node values available');
            return;
        }
        
        const maxNodeValue = Math.max(...nodeValues);
        const minNodeValue = Math.min(...nodeValues);
        const nodeValueRange = maxNodeValue - minNodeValue;
        
        const edgeValues = coattendanceGraphData.edges && Array.isArray(coattendanceGraphData.edges) 
            ? coattendanceGraphData.edges.map(e => e.value || 1)
            : [];
        const maxEdgeValue = edgeValues.length > 0 ? Math.max(...edgeValues) : 1;
        const minEdgeValue = edgeValues.length > 0 ? Math.min(...edgeValues) : 1;
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
            id: node.id,
            label: node.label || node.id,
            value: degree,
            title: node.title || `${node.id} - Degree: ${degree}`,
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
    const edgesData = coattendanceGraphData.edges && Array.isArray(coattendanceGraphData.edges) 
        ? coattendanceGraphData.edges 
        : [];
    
    const scaledEdges = edgesData.map(edge => {
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
            from: edge.from,
            to: edge.to,
            value: weight,
            width: width,
            title: edge.title || `Co-attended ${weight} time(s)`,
            color: {
                color: `rgba(3, 102, 214, ${opacity})`,
                highlight: '#0366d6',
                hover: '#0366d6'
            },
            smooth: {
                type: 'continuous',
                roundness: 0.5
            }
        };
    });
    
    const nodes = new vis.DataSet(scaledNodes);
    const edges = new vis.DataSet(scaledEdges);
    
    // Store references to all nodes and edges for filtering
    const allNodeIds = new Set(scaledNodes.map(n => n.id));
    const allEdgeIds = new Set(scaledEdges.map(e => `${e.from}-${e.to}`));
    let currentlySelectedNodeId = null;
    
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
                iterations: 150,
                updateInterval: 100,
                onlyDynamicEdges: false,
                fit: true
            },
            barnesHut: {
                gravitationalConstant: -5000,
                centralGravity: 0.05,
                springLength: 250,
                springConstant: 0.01,
                damping: 0.5,
                avoidOverlap: 1.2
            },
            maxVelocity: 5,
            minVelocity: 0.1,
            solver: 'barnesHut',
            timestep: 0.3
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
    
    // Disable physics after stabilization to prevent constant movement
    let physicsDisabled = false;
    
    coattendanceNetwork.once('stabilizationEnd', function() {
        if (!physicsDisabled) {
            physicsDisabled = true;
            console.log('Network stabilized - disabling physics');
            coattendanceNetwork.setOptions({
                physics: {
                    enabled: false
                }
            });
        }
    });
    
    // Fallback: disable physics after 3 seconds regardless of stabilization status
    setTimeout(function() {
        if (!physicsDisabled) {
            physicsDisabled = true;
            console.log('Force disabling physics after timeout');
            coattendanceNetwork.setOptions({
                physics: {
                    enabled: false
                }
            });
        }
    }, 3000);
    
    // Function to filter visualization to show only selected node and its connections
    function filterToNode(nodeId) {
        if (!nodeId) {
            // Reset: show all nodes and edges
            const allNodeIdsArray = Array.from(allNodeIds);
            allNodeIdsArray.forEach(id => {
                nodes.update({ id: id, hidden: false });
            });
            
            // Remove all edges and re-add them
            edges.clear();
            edges.add(scaledEdges);
            
            currentlySelectedNodeId = null;
            console.log('Reset to full view');
            return;
        }
        
        currentlySelectedNodeId = nodeId;
        
        // Find all edges connected to this node
        const connectedEdges = scaledEdges.filter(e => 
            e.from === nodeId || e.to === nodeId
        );
        
        // Get all connected node IDs (the selected node + its neighbors)
        const connectedNodeIds = new Set([nodeId]);
        connectedEdges.forEach(e => {
            connectedNodeIds.add(e.from);
            connectedNodeIds.add(e.to);
        });
        
        // Hide all nodes except connected ones
        allNodeIds.forEach(id => {
            nodes.update({ 
                id: id, 
                hidden: !connectedNodeIds.has(id)
            });
        });
        
        // Replace edges with only connected ones
        edges.clear();
        edges.add(connectedEdges);
        
        console.log(`Filtered to node: ${nodeId} (showing ${connectedNodeIds.size} nodes, ${connectedEdges.length} edges)`);
    }
    
    // Add event listeners for better interactivity
    coattendanceNetwork.on('click', function(params) {
        if (params.nodes.length > 0) {
            const nodeId = params.nodes[0];
            const node = coattendanceGraphData.nodes.find(n => n.id === nodeId);
            
            // If clicking the same node again, reset to full view
            if (currentlySelectedNodeId === nodeId) {
                filterToNode(null); // Reset view
                return;
            }
            
            // Filter to show only this node and its connections
            filterToNode(nodeId);
        } else if (params.nodes.length === 0 && currentlySelectedNodeId) {
            // Clicking on background: reset to full view
            filterToNode(null);
        }
    });
    
    coattendanceNetwork.on('hoverNode', function(params) {
        container.style.cursor = 'pointer';
    });
    
    coattendanceNetwork.on('blurNode', function(params) {
        container.style.cursor = 'default';
    });
    
    // Optionally re-enable physics temporarily when dragging nodes
    coattendanceNetwork.on('dragStart', function(params) {
        // Physics can remain disabled during drag for stability
    });
    
    console.log('Network visualization initialized successfully');
    } catch (error) {
        console.error('Error initializing network visualization:', error);
        const container = document.getElementById('coattendance-network');
        if (container) {
            container.innerHTML = '<p style="color: red; padding: 20px;">Error loading network visualization. Please check the browser console for details.</p>';
        }
    }
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
        'components': 'Components',
        'audit': 'Audit'
    };
    
    tabButtons.forEach(button => {
        if (button.textContent.trim() === tabMap[tabId]) {
            button.classList.add('active');
        }
    });

    // Initialize network visualization if showing co-attendance tab
    if (tabId === 'coattendance') {
        // Delay to ensure DOM is ready and tab is visible
        setTimeout(() => {
            initCoattendanceNetwork();
        }, 200);
    } else if (coattendanceNetwork) {
        // Destroy network when switching away from co-attendance tab
        try {
            coattendanceNetwork.destroy();
            coattendanceNetwork = null;
        } catch (e) {
            console.error('Error destroying network:', e);
        }
    }
    
    // Load audit data if showing audit tab
    if (tabId === 'audit') {
        setTimeout(() => {
            loadAuditData();
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
        const validTabs = ['summary', 'coattendance', 'field-degree', 'path-structure', 'centrality', 'clustering', 'components', 'audit'];
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
        const validTabs = ['summary', 'coattendance', 'field-degree', 'path-structure', 'centrality', 'clustering', 'components', 'audit'];
        if (validTabs.includes(hash)) {
            showTab(hash);
        }
    }
});

// Review management functions
const REVIEWS_STORAGE_KEY = 'analysis_reviews';
const REVIEWS_JSON_URL = 'audit/reviews.json';

// Load reviews from localStorage
function loadReviewsFromStorage() {
    try {
        const reviewsJson = localStorage.getItem(REVIEWS_STORAGE_KEY);
        return reviewsJson ? JSON.parse(reviewsJson) : [];
    } catch (error) {
        console.error('Error loading reviews from localStorage:', error);
        return [];
    }
}

// Save reviews to localStorage
function saveReviewsToStorage(reviews) {
    try {
        localStorage.setItem(REVIEWS_STORAGE_KEY, JSON.stringify(reviews));
    } catch (error) {
        console.error('Error saving reviews to localStorage:', error);
    }
}

// Load reviews from JSON file
async function loadReviewsFromJSON() {
    try {
        const response = await fetch(REVIEWS_JSON_URL);
        if (!response.ok) {
            return { methods: {}, last_updated: null };
        }
        return await response.json();
    } catch (error) {
        console.error('Error loading reviews from JSON:', error);
        return { methods: {}, last_updated: null };
    }
}

// Submit review form
function submitReview(event, methodName) {
    event.preventDefault();
    
    const form = document.getElementById(`review-form-${methodName}`);
    const formData = new FormData(form);
    
    const review = {
        id: Date.now().toString(),
        method: methodName,
        rating: formData.get('rating'),
        comment: formData.get('comment'),
        reviewer: formData.get('reviewer') || 'Anonymous',
        suggestions: formData.get('suggestions') || '',
        file: formData.get('file'),
        timestamp: new Date().toISOString()
    };
    
    // Save to localStorage
    const reviews = loadReviewsFromStorage();
    reviews.push(review);
    saveReviewsToStorage(reviews);
    
    // Show success message
    const successDiv = document.getElementById(`review-success-${methodName}`);
    if (successDiv) {
        successDiv.style.display = 'block';
    }
    
    // Reset form
    form.reset();
    
    // Update reviews list
    displayReviewsForMethod(methodName);
    
    // Update audit tab if visible
    if (document.getElementById('audit').classList.contains('active')) {
        loadAuditData();
    }
    
    return false;
}

// Display reviews for a specific method
function displayReviewsForMethod(methodName) {
    const reviewsList = document.getElementById(`reviews-list-${methodName}`);
    if (!reviewsList) return;
    
    const allReviews = loadReviewsFromStorage();
    const methodReviews = allReviews.filter(r => r.method === methodName);
    
    if (methodReviews.length === 0) {
        reviewsList.innerHTML = '<p style="color: #586069; font-size: 0.9em;">No reviews yet. Be the first to submit a review!</p>';
        return;
    }
    
    reviewsList.innerHTML = '<h4>Previous Reviews</h4>' + methodReviews.map(review => {
        const date = new Date(review.timestamp).toLocaleString();
        return `
            <div class="review-item rating-${review.rating}">
                <div class="review-item-header">
                    <span class="review-item-rating rating-${review.rating}">${review.rating.toUpperCase()}</span>
                    <span class="review-item-meta">${review.reviewer} • ${date}</span>
                </div>
                <div class="review-item-comment">${escapeHtml(review.comment)}</div>
                ${review.suggestions ? `<div class="review-item-suggestions"><strong>Suggestions:</strong> ${escapeHtml(review.suggestions)}</div>` : ''}
            </div>
        `;
    }).join('');
}

// Escape HTML to prevent XSS
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

// Download review as JSON
function downloadReviewJSON(methodName) {
    const allReviews = loadReviewsFromStorage();
    const methodReviews = allReviews.filter(r => r.method === methodName);
    
    const dataStr = JSON.stringify(methodReviews, null, 2);
    const dataBlob = new Blob([dataStr], { type: 'application/json' });
    const url = URL.createObjectURL(dataBlob);
    const link = document.createElement('a');
    link.href = url;
    link.download = `review_${methodName}_${Date.now()}.json`;
    link.click();
    URL.revokeObjectURL(url);
}

// Load and display reviews when tab is shown
function loadReviewsForTab(methodName) {
    displayReviewsForMethod(methodName);
}

// Update audit tab to show reviews
async function loadAuditData() {
    const auditTab = document.getElementById('audit');
    if (!auditTab || !auditTab.classList.contains('active')) {
        return;
    }
    
    // Load from localStorage
    const localReviews = loadReviewsFromStorage();
    
    // Load from JSON file
    const jsonData = await loadReviewsFromJSON();
    
    // Combine both sources
    const allReviews = [...localReviews];
    if (jsonData.methods) {
        Object.keys(jsonData.methods).forEach(method => {
            if (jsonData.methods[method].reviews) {
                jsonData.methods[method].reviews.forEach(review => {
                    // Avoid duplicates
                    if (!allReviews.find(r => r.id === review.id)) {
                        allReviews.push(review);
                    }
                });
            }
        });
    }
    
    // Group by method
    const reviewsByMethod = {};
    const methodStats = {};
    
    ['coattendance', 'field-degree', 'path-structure', 'centrality', 'clustering', 'components'].forEach(method => {
        const methodReviews = allReviews.filter(r => r.method === method);
        reviewsByMethod[method] = methodReviews;
        
        const stats = {
            total: methodReviews.length,
            correct: methodReviews.filter(r => r.rating === 'correct').length,
            incorrect: methodReviews.filter(r => r.rating === 'incorrect').length,
            needs_review: methodReviews.filter(r => r.rating === 'needs-review').length,
            trust_score: 0
        };
        
        if (stats.total > 0) {
            stats.trust_score = ((stats.correct - stats.incorrect) / stats.total + 1) / 2;
        }
        
        methodStats[method] = stats;
    });
    
    // Display audit data
    displayAuditData(methodStats, reviewsByMethod, jsonData.last_updated);
}

// Display audit data in the audit tab
function displayAuditData(methodStats, reviewsByMethod, lastUpdated) {
    const auditTab = document.getElementById('audit');
    if (!auditTab) return;
    
    let html = '<h2>Community Review Audit</h2>';
    
    if (lastUpdated) {
        html += `<p class="explanation">Last updated from JSON: ${new Date(lastUpdated).toLocaleString()}</p>`;
    }
    
    html += '<div class="audit-stats">';
    Object.keys(methodStats).forEach(method => {
        const stats = methodStats[method];
        const methodName = method.replace('-', ' ').replace(/\b\w/g, l => l.toUpperCase());
        html += `
            <div class="method-stat-card">
                <h3>${methodName}</h3>
                <div class="stat-row">
                    <span>Total Reviews:</span>
                    <strong>${stats.total}</strong>
                </div>
                <div class="stat-row">
                    <span>Trust Score:</span>
                    <strong>${(stats.trust_score * 100).toFixed(1)}%</strong>
                </div>
                <div class="stat-row">
                    <span>Ratings:</span>
                    <span>✓ ${stats.correct} | ? ${stats.needs_review} | ✗ ${stats.incorrect}</span>
                </div>
            </div>
        `;
    });
    html += '</div>';
    
    html += '<h3>All Reviews</h3>';
    Object.keys(reviewsByMethod).forEach(method => {
        const reviews = reviewsByMethod[method];
        if (reviews.length === 0) return;
        
        const methodName = method.replace('-', ' ').replace(/\b\w/g, l => l.toUpperCase());
        html += `<h4>${methodName}</h4>`;
        html += reviews.map(review => {
            const date = new Date(review.timestamp).toLocaleString();
            return `
                <div class="review-item rating-${review.rating}">
                    <div class="review-item-header">
                        <span class="review-item-rating rating-${review.rating}">${review.rating.toUpperCase()}</span>
                        <span class="review-item-meta">${review.reviewer} • ${date}</span>
                    </div>
                    <div class="review-item-comment">${escapeHtml(review.comment)}</div>
                    ${review.suggestions ? `<div class="review-item-suggestions"><strong>Suggestions:</strong> ${escapeHtml(review.suggestions)}</div>` : ''}
                </div>
            `;
        }).join('');
    });
    
    auditTab.innerHTML = html;
}

// Store original showTab function
let originalShowTab = showTab;

// Override showTab to load reviews when switching tabs
function showTabWithReviews(tabId) {
    // Call original showTab
    originalShowTab(tabId);
    
    // Load reviews for the current tab
    setTimeout(() => {
        const validMethods = ['coattendance', 'field-degree', 'path-structure', 'centrality', 'clustering', 'components'];
        if (validMethods.includes(tabId)) {
            loadReviewsForTab(tabId);
        } else if (tabId === 'audit') {
            loadAuditData();
        }
    }, 100);
}

// Replace showTab
showTab = showTabWithReviews;

// Load reviews on page load
document.addEventListener('DOMContentLoaded', function() {
    // Load reviews for initial tab
    const activeTab = document.querySelector('.tab-pane.active');
    if (activeTab) {
        const tabId = activeTab.id;
        if (tabId && tabId !== 'summary') {
            if (tabId === 'audit') {
                loadAuditData();
            } else {
                loadReviewsForTab(tabId);
            }
        }
    }
});

