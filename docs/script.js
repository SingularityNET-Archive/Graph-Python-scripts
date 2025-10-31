// Chart initialization functions
function initSummaryChart() {
    if (!chartData || !chartData.summary) return;
    
    const labels = Object.keys(chartData.summary);
    const values = Object.values(chartData.summary);
    
    const trace = {
        x: labels,
        y: values,
        type: 'bar',
        marker: { color: '#0366d6' }
    };
    
    const layout = {
        title: 'Graph Statistics',
        xaxis: { title: 'Metric' },
        yaxis: { title: 'Count' },
        height: 300,
        margin: { l: 60, r: 20, t: 50, b: 80 }
    };
    
    Plotly.newPlot('summary-chart', [trace], layout, {responsive: true});
}

function initCoattendanceTopChart() {
    if (!chartData || !chartData.coattendanceTop) return;
    
    const nodes = chartData.coattendanceTop.map(d => d.node);
    const degrees = chartData.coattendanceTop.map(d => d.degree);
    
    const trace = {
        x: nodes,
        y: degrees,
        type: 'bar',
        marker: { color: '#28a745' }
    };
    
    const layout = {
        title: 'Top Nodes by Degree',
        xaxis: { title: 'Participant', tickangle: -45 },
        yaxis: { title: 'Degree' },
        height: 400,
        margin: { l: 60, r: 20, t: 50, b: 120 }
    };
    
    Plotly.newPlot('coattendance-top-chart', [trace], layout, {responsive: true});
}

function initCoattendanceDistChart() {
    if (!chartData || !chartData.coattendanceDist) return;
    
    const degrees = chartData.coattendanceDist.map(d => d.degree);
    const counts = chartData.coattendanceDist.map(d => d.count);
    
    const trace = {
        x: degrees,
        y: counts,
        type: 'bar',
        marker: { color: '#17a2b8' }
    };
    
    const layout = {
        title: 'Degree Distribution',
        xaxis: { title: 'Degree' },
        yaxis: { title: 'Count of Nodes' },
        height: 300,
        margin: { l: 60, r: 20, t: 50, b: 60 }
    };
    
    Plotly.newPlot('coattendance-dist-chart', [trace], layout, {responsive: true});
}

function initFieldDegreeTopChart() {
    if (!chartData || !chartData.fieldDegreeTop) return;
    
    const fields = chartData.fieldDegreeTop.map(d => d.field);
    const degrees = chartData.fieldDegreeTop.map(d => d.degree);
    
    const trace = {
        x: fields,
        y: degrees,
        type: 'bar',
        marker: { color: '#ffc107' }
    };
    
    const layout = {
        title: 'Top Fields by Degree',
        xaxis: { title: 'Field', tickangle: -45 },
        yaxis: { title: 'Degree' },
        height: 400,
        margin: { l: 60, r: 20, t: 50, b: 120 }
    };
    
    Plotly.newPlot('field-degree-top-chart', [trace], layout, {responsive: true});
}

function initFieldDegreeDistChart() {
    if (!chartData || !chartData.fieldDegreeDist) return;
    
    const degrees = chartData.fieldDegreeDist.map(d => d.degree);
    const counts = chartData.fieldDegreeDist.map(d => d.count);
    
    const trace = {
        x: degrees,
        y: counts,
        type: 'bar',
        marker: { color: '#fd7e14' }
    };
    
    const layout = {
        title: 'Field Degree Distribution',
        xaxis: { title: 'Degree' },
        yaxis: { title: 'Count of Fields' },
        height: 300,
        margin: { l: 60, r: 20, t: 50, b: 60 }
    };
    
    Plotly.newPlot('field-degree-dist-chart', [trace], layout, {responsive: true});
}

function initPathStructureChart() {
    if (!chartData || !chartData.pathStructure) return;
    
    const parents = chartData.pathStructure.map(d => d.parent.substring(0, 40) + '...');
    const counts = chartData.pathStructure.map(d => d.count);
    
    const trace = {
        x: counts,
        y: parents,
        type: 'bar',
        orientation: 'h',
        marker: { color: '#6f42c1' }
    };
    
    const layout = {
        title: 'Most Common Parent Paths',
        xaxis: { title: 'Count' },
        yaxis: { title: 'Parent Path' },
        height: 400,
        margin: { l: 200, r: 20, t: 50, b: 60 }
    };
    
    Plotly.newPlot('path-structure-chart', [trace], layout, {responsive: true});
}

function initCentralityChart() {
    if (!chartData || !chartData.centrality) return;
    
    const fields = chartData.centrality.map(d => d.field);
    const degree = chartData.centrality.map(d => d.degree);
    const betweenness = chartData.centrality.map(d => d.betweenness);
    const closeness = chartData.centrality.map(d => d.closeness);
    const eigenvector = chartData.centrality.map(d => d.eigenvector);
    
    const traces = [
        { name: 'Degree', x: fields, y: degree, type: 'scatter', mode: 'markers+lines', marker: { size: 10 } },
        { name: 'Betweenness', x: fields, y: betweenness, type: 'scatter', mode: 'markers+lines', marker: { size: 10 } },
        { name: 'Closeness', x: fields, y: closeness, type: 'scatter', mode: 'markers+lines', marker: { size: 10 } },
        { name: 'Eigenvector', x: fields, y: eigenvector, type: 'scatter', mode: 'markers+lines', marker: { size: 10 } }
    ];
    
    const layout = {
        title: 'Centrality Metrics Comparison',
        xaxis: { title: 'Field', tickangle: -45 },
        yaxis: { title: 'Centrality Score' },
        height: 500,
        margin: { l: 60, r: 20, t: 50, b: 120 },
        legend: { x: 1, y: 1 }
    };
    
    Plotly.newPlot('centrality-chart', traces, layout, {responsive: true});
}

function initClusteringChart() {
    if (!chartData || !chartData.clustering) return;
    
    const fields = chartData.clustering.map(d => d.field);
    const clustering = chartData.clustering.map(d => d.clustering);
    
    const trace = {
        x: fields,
        y: clustering,
        type: 'bar',
        marker: { color: '#dc3545' }
    };
    
    const layout = {
        title: 'Top Nodes by Clustering Coefficient',
        xaxis: { title: 'Field', tickangle: -45 },
        yaxis: { title: 'Clustering Coefficient' },
        height: 400,
        margin: { l: 60, r: 20, t: 50, b: 120 }
    };
    
    Plotly.newPlot('clustering-chart', [trace], layout, {responsive: true});
}

function initComponentsChart() {
    if (!chartData || !chartData.components || !chartData.components.sizes) return;
    
    const sizes = chartData.components.sizes;
    const indices = sizes.map((_, i) => `Component ${i + 1}`);
    
    const trace = {
        x: indices,
        y: sizes,
        type: 'bar',
        marker: { color: '#20c997' }
    };
    
    const layout = {
        title: 'Component Sizes',
        xaxis: { title: 'Component' },
        yaxis: { title: 'Size (number of fields)' },
        height: 300,
        margin: { l: 60, r: 20, t: 50, b: 60 }
    };
    
    Plotly.newPlot('components-chart', [trace], layout, {responsive: true});
}

// Initialize charts when tab is shown
function initChartsForTab(tabId) {
    switch(tabId) {
        case 'summary':
            initSummaryChart();
            break;
        case 'coattendance':
            initCoattendanceTopChart();
            initCoattendanceDistChart();
            break;
        case 'field-degree':
            initFieldDegreeTopChart();
            initFieldDegreeDistChart();
            break;
        case 'path-structure':
            initPathStructureChart();
            break;
        case 'centrality':
            initCentralityChart();
            break;
        case 'clustering':
            initClusteringChart();
            break;
        case 'components':
            initComponentsChart();
            break;
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
        'components': 'Components'
    };
    
    tabButtons.forEach(button => {
        if (button.textContent.trim() === tabMap[tabId]) {
            button.classList.add('active');
        }
    });

    // Initialize charts for this tab
    initChartsForTab(tabId);

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
    
    // Initialize charts for the initial tab (showTab already does this, but ensure it happens)
    setTimeout(() => {
        const initialTab = hash && ['summary', 'coattendance', 'field-degree', 'path-structure', 'centrality', 'clustering', 'components'].includes(hash) ? hash : 'summary';
        initChartsForTab(initialTab);
    }, 100);
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

