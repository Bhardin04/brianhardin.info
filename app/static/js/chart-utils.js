/**
 * Advanced Chart Utilities for Interactive Demos
 * Provides drill-down, filtering, zoom, and export capabilities
 */

class AdvancedChartManager {
    constructor() {
        this.charts = new Map();
        this.chartConfigs = new Map();
        this.drillDownStacks = new Map();
        this.filters = new Map();
        this.exportQueue = [];
    }

    /**
     * Register a chart with advanced capabilities
     */
    registerChart(chartId, chartInstance, config = {}) {
        this.charts.set(chartId, chartInstance);
        this.chartConfigs.set(chartId, {
            allowDrillDown: config.allowDrillDown || false,
            allowZoom: config.allowZoom || false,
            allowFiltering: config.allowFiltering || false,
            allowExport: config.allowExport || false,
            drillDownLevels: config.drillDownLevels || [],
            ...config
        });

        this.drillDownStacks.set(chartId, []);
        this.filters.set(chartId, {});

        // Add event listeners if enabled
        this.setupChartInteractions(chartId, chartInstance);

        console.log(`Advanced chart registered: ${chartId}`, config);
    }

    /**
     * Setup interactive event listeners
     */
    setupChartInteractions(chartId, chart) {
        const config = this.chartConfigs.get(chartId);

        // Drill-down on click
        if (config.allowDrillDown) {
            chart.options.onClick = (event, elements) => {
                if (elements.length > 0) {
                    this.handleDrillDown(chartId, elements[0]);
                }
            };
        }

        // Zoom functionality
        if (config.allowZoom) {
            chart.options.plugins = chart.options.plugins || {};
            chart.options.plugins.zoom = {
                zoom: {
                    wheel: {
                        enabled: true,
                    },
                    pinch: {
                        enabled: true
                    },
                    mode: 'xy',
                },
                pan: {
                    enabled: true,
                    mode: 'xy',
                }
            };
        }

        // Custom tooltip with drill-down hint
        if (config.allowDrillDown) {
            chart.options.plugins = chart.options.plugins || {};
            chart.options.plugins.tooltip = {
                ...chart.options.plugins.tooltip,
                footer: (tooltipItems) => {
                    return 'Click to drill down';
                }
            };
        }
    }

    /**
     * Handle drill-down functionality
     */
    async handleDrillDown(chartId, element) {
        const chart = this.charts.get(chartId);
        const config = this.chartConfigs.get(chartId);
        const stack = this.drillDownStacks.get(chartId);

        if (!config.allowDrillDown) return;

        const dataIndex = element.index;
        const datasetIndex = element.datasetIndex;
        const currentLevel = stack.length;

        if (currentLevel >= config.drillDownLevels.length) return;

        // Store current state for back navigation
        stack.push({
            data: chart.data,
            options: chart.options,
            level: currentLevel,
            selectedIndex: dataIndex,
            selectedLabel: chart.data.labels[dataIndex]
        });

        // Show loading state
        this.showChartLoading(chartId);

        try {
            // Get drill-down data
            const drillDownData = await this.fetchDrillDownData(
                chartId,
                config.drillDownLevels[currentLevel],
                dataIndex,
                chart.data.labels[dataIndex]
            );

            // Update chart with new data
            this.updateChartData(chartId, drillDownData);

            // Add back button if not present
            this.addBackButton(chartId);

            // Trigger drill-down event
            this.triggerChartEvent(chartId, 'drilldown', {
                level: currentLevel + 1,
                selectedItem: chart.data.labels[dataIndex],
                newData: drillDownData
            });

        } catch (error) {
            console.error('Drill-down failed:', error);
            this.showChartError(chartId, 'Failed to load drill-down data');
            // Remove the failed state from stack
            stack.pop();
        }
    }

    /**
     * Navigate back in drill-down hierarchy
     */
    drillUp(chartId) {
        const stack = this.drillDownStacks.get(chartId);

        if (stack.length === 0) return;

        const previousState = stack.pop();
        this.updateChartData(chartId, previousState.data, previousState.options);

        // Remove back button if at top level
        if (stack.length === 0) {
            this.removeBackButton(chartId);
        }

        this.triggerChartEvent(chartId, 'drillup', {
            level: stack.length,
            restoredData: previousState.data
        });
    }

    /**
     * Apply filters to chart data
     */
    applyFilter(chartId, filterKey, filterValue) {
        const filters = this.filters.get(chartId);
        const chart = this.charts.get(chartId);

        if (filterValue === null || filterValue === '') {
            delete filters[filterKey];
        } else {
            filters[filterKey] = filterValue;
        }

        // Get original data (from bottom of drill-down stack or current)
        const stack = this.drillDownStacks.get(chartId);
        const originalData = stack.length > 0 ? stack[0].data : chart.data;

        // Apply all active filters
        const filteredData = this.filterChartData(originalData, filters);

        // Update chart
        this.updateChartData(chartId, filteredData);

        this.triggerChartEvent(chartId, 'filter', {
            appliedFilters: filters,
            filteredData: filteredData
        });
    }

    /**
     * Filter chart data based on active filters
     */
    filterChartData(data, filters) {
        const filteredData = JSON.parse(JSON.stringify(data)); // Deep copy

        if (Object.keys(filters).length === 0) {
            return filteredData;
        }

        // Apply filters to datasets
        filteredData.datasets = filteredData.datasets.map(dataset => {
            const filteredDataset = { ...dataset };

            // Filter data points based on labels and values
            const filteredIndices = [];

            data.labels.forEach((label, index) => {
                let includePoint = true;

                // Apply each filter
                Object.entries(filters).forEach(([filterKey, filterValue]) => {
                    switch (filterKey) {
                        case 'minValue':
                            if (dataset.data[index] < parseFloat(filterValue)) {
                                includePoint = false;
                            }
                            break;
                        case 'maxValue':
                            if (dataset.data[index] > parseFloat(filterValue)) {
                                includePoint = false;
                            }
                            break;
                        case 'labelContains':
                            if (!label.toLowerCase().includes(filterValue.toLowerCase())) {
                                includePoint = false;
                            }
                            break;
                        case 'category':
                            // Custom category filtering logic
                            if (dataset.categories && dataset.categories[index] !== filterValue) {
                                includePoint = false;
                            }
                            break;
                    }
                });

                if (includePoint) {
                    filteredIndices.push(index);
                }
            });

            // Update data and labels
            filteredDataset.data = filteredIndices.map(i => dataset.data[i]);
            if (filteredIndices.length < data.labels.length) {
                filteredData.labels = filteredIndices.map(i => data.labels[i]);
            }

            return filteredDataset;
        });

        return filteredData;
    }

    /**
     * Update chart with new data
     */
    updateChartData(chartId, newData, newOptions = null) {
        const chart = this.charts.get(chartId);

        // Update data
        chart.data = newData;

        // Update options if provided
        if (newOptions) {
            chart.options = newOptions;
        }

        // Update chart
        chart.update('active');
    }

    /**
     * Fetch drill-down data (mock implementation)
     */
    async fetchDrillDownData(chartId, drillLevel, selectedIndex, selectedLabel) {
        // Simulate API call delay
        await new Promise(resolve => setTimeout(resolve, 500));

        // Mock drill-down data generation
        return this.generateMockDrillDownData(drillLevel, selectedLabel);
    }

    /**
     * Generate mock drill-down data
     */
    generateMockDrillDownData(drillLevel, selectedLabel) {
        const drillDownTypes = {
            'monthly': {
                labels: ['Week 1', 'Week 2', 'Week 3', 'Week 4'],
                datasets: [{
                    label: `${selectedLabel} - Weekly Breakdown`,
                    data: Array.from({length: 4}, () => Math.floor(Math.random() * 50000) + 10000),
                    backgroundColor: 'rgba(147, 51, 234, 0.8)',
                    borderColor: 'rgb(147, 51, 234)',
                    borderWidth: 1
                }]
            },
            'quarterly': {
                labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
                datasets: [{
                    label: `${selectedLabel} - Monthly Breakdown`,
                    data: Array.from({length: 12}, () => Math.floor(Math.random() * 200000) + 50000),
                    backgroundColor: 'rgba(59, 130, 246, 0.8)',
                    borderColor: 'rgb(59, 130, 246)',
                    borderWidth: 1
                }]
            },
            'customer': {
                labels: ['Product A', 'Product B', 'Product C', 'Product D', 'Product E'],
                datasets: [{
                    label: `${selectedLabel} - Product Revenue`,
                    data: Array.from({length: 5}, () => Math.floor(Math.random() * 100000) + 20000),
                    backgroundColor: [
                        'rgba(34, 197, 94, 0.8)',
                        'rgba(251, 146, 60, 0.8)',
                        'rgba(239, 68, 68, 0.8)',
                        'rgba(168, 85, 247, 0.8)',
                        'rgba(14, 165, 233, 0.8)'
                    ],
                    borderWidth: 1
                }]
            }
        };

        return drillDownTypes[drillLevel] || drillDownTypes['monthly'];
    }

    /**
     * Export chart data to various formats
     */
    async exportChart(chartId, format = 'png', options = {}) {
        const chart = this.charts.get(chartId);
        const config = this.chartConfigs.get(chartId);

        if (!config.allowExport) {
            throw new Error('Export not allowed for this chart');
        }

        this.addToExportQueue(chartId, format);

        try {
            switch (format.toLowerCase()) {
                case 'png':
                case 'jpg':
                case 'jpeg':
                    return await this.exportChartAsImage(chart, format, options);
                case 'pdf':
                    return await this.exportChartAsPDF(chart, options);
                case 'csv':
                    return await this.exportChartAsCSV(chart, options);
                case 'excel':
                    return await this.exportChartAsExcel(chart, options);
                default:
                    throw new Error(`Unsupported export format: ${format}`);
            }
        } finally {
            this.removeFromExportQueue(chartId, format);
        }
    }

    /**
     * Export chart as image
     */
    async exportChartAsImage(chart, format, options) {
        const canvas = chart.canvas;
        const dataURL = canvas.toDataURL(`image/${format}`, options.quality || 0.9);

        // Create download link
        const link = document.createElement('a');
        link.download = `chart_${Date.now()}.${format}`;
        link.href = dataURL;

        // Trigger download
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);

        return dataURL;
    }

    /**
     * Export chart as CSV
     */
    async exportChartAsCSV(chart, options) {
        const data = chart.data;
        let csvContent = "data:text/csv;charset=utf-8,";

        // Headers
        const headers = ['Label', ...data.datasets.map(ds => ds.label)];
        csvContent += headers.join(',') + '\n';

        // Data rows
        data.labels.forEach((label, index) => {
            const row = [label, ...data.datasets.map(ds => ds.data[index] || 0)];
            csvContent += row.join(',') + '\n';
        });

        // Create download link
        const encodedUri = encodeURI(csvContent);
        const link = document.createElement('a');
        link.download = `chart_data_${Date.now()}.csv`;
        link.href = encodedUri;

        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);

        return csvContent;
    }

    /**
     * Export chart as PDF
     */
    async exportChartAsPDF(chart, options) {
        // We'll use jsPDF with chart image
        if (!window.jsPDF) {
            // Load jsPDF dynamically if not available
            await this.loadScript('https://cdnjs.cloudflare.com/ajax/libs/jspdf/2.5.1/jspdf.umd.min.js');
        }

        const { jsPDF } = window;
        const pdf = new jsPDF({
            orientation: options.orientation || 'landscape',
            unit: 'mm',
            format: options.format || 'a4'
        });

        // Get chart image
        const canvas = chart.canvas;
        const imgData = canvas.toDataURL('image/png', 0.9);

        // Calculate dimensions
        const pageWidth = pdf.internal.pageSize.getWidth();
        const pageHeight = pdf.internal.pageSize.getHeight();
        const margin = 20;
        const maxWidth = pageWidth - (margin * 2);
        const maxHeight = pageHeight - (margin * 3) - 20; // Extra space for title

        // Calculate aspect ratio
        const imgAspectRatio = canvas.width / canvas.height;
        let imgWidth = maxWidth;
        let imgHeight = imgWidth / imgAspectRatio;

        // Adjust if height exceeds page
        if (imgHeight > maxHeight) {
            imgHeight = maxHeight;
            imgWidth = imgHeight * imgAspectRatio;
        }

        // Add title
        pdf.setFontSize(16);
        pdf.setFont(undefined, 'bold');
        const title = options.title || 'Chart Export';
        pdf.text(title, margin, margin);

        // Add timestamp
        pdf.setFontSize(10);
        pdf.setFont(undefined, 'normal');
        const timestamp = `Generated on ${new Date().toLocaleDateString()} at ${new Date().toLocaleTimeString()}`;
        pdf.text(timestamp, margin, margin + 8);

        // Add chart image
        const yPosition = margin + 20;
        pdf.addImage(imgData, 'PNG', margin, yPosition, imgWidth, imgHeight);

        // Add data table if requested
        if (options.includeData && chart.data) {
            const tableY = yPosition + imgHeight + 10;
            this.addDataTableToPDF(pdf, chart.data, margin, tableY, maxWidth);
        }

        // Add footer
        pdf.setFontSize(8);
        pdf.setFont(undefined, 'normal');
        const footerY = pageHeight - 10;
        pdf.text('Generated by Brian Hardin Interactive Demos', margin, footerY);

        // Save PDF
        const filename = options.filename || `chart_export_${Date.now()}.pdf`;
        pdf.save(filename);

        return pdf;
    }

    /**
     * Add data table to PDF
     */
    addDataTableToPDF(pdf, chartData, x, y, maxWidth) {
        if (!chartData.labels || !chartData.datasets) return;

        const rowHeight = 6;
        const colWidth = maxWidth / (chartData.datasets.length + 1);

        // Headers
        pdf.setFont(undefined, 'bold');
        pdf.text('Label', x, y);
        chartData.datasets.forEach((dataset, index) => {
            pdf.text(dataset.label || `Dataset ${index + 1}`, x + (colWidth * (index + 1)), y);
        });

        // Data rows
        pdf.setFont(undefined, 'normal');
        chartData.labels.forEach((label, rowIndex) => {
            const rowY = y + (rowHeight * (rowIndex + 1));
            pdf.text(String(label), x, rowY);

            chartData.datasets.forEach((dataset, colIndex) => {
                const value = dataset.data[rowIndex] || 0;
                const formattedValue = typeof value === 'number' ? value.toLocaleString() : String(value);
                pdf.text(formattedValue, x + (colWidth * (colIndex + 1)), rowY);
            });
        });
    }

    /**
     * Export chart as Excel
     */
    async exportChartAsExcel(chart, options) {
        // We'll use SheetJS for Excel export
        if (!window.XLSX) {
            await this.loadScript('https://cdnjs.cloudflare.com/ajax/libs/xlsx/0.18.5/xlsx.full.min.js');
        }

        const XLSX = window.XLSX;
        const workbook = XLSX.utils.book_new();

        // Create data worksheet
        const data = chart.data;
        const worksheetData = [];

        // Headers
        const headers = ['Label', ...data.datasets.map(ds => ds.label || 'Data')];
        worksheetData.push(headers);

        // Data rows
        data.labels.forEach((label, index) => {
            const row = [label, ...data.datasets.map(ds => ds.data[index] || 0)];
            worksheetData.push(row);
        });

        // Create worksheet
        const worksheet = XLSX.utils.aoa_to_sheet(worksheetData);

        // Style headers
        const headerRange = XLSX.utils.decode_range(worksheet['!ref']);
        for (let col = headerRange.s.c; col <= headerRange.e.c; col++) {
            const cellRef = XLSX.utils.encode_cell({ r: 0, c: col });
            if (worksheet[cellRef]) {
                worksheet[cellRef].s = {
                    font: { bold: true },
                    fill: { fgColor: { rgb: 'EEEEEE' } }
                };
            }
        }

        // Set column widths
        const colWidths = headers.map(header => ({ wch: Math.max(header.length, 15) }));
        worksheet['!cols'] = colWidths;

        // Add worksheet to workbook
        XLSX.utils.book_append_sheet(workbook, worksheet, 'Chart Data');

        // Add metadata worksheet if requested
        if (options.includeMetadata) {
            const metadataSheet = this.createMetadataSheet(chart, options);
            XLSX.utils.book_append_sheet(workbook, metadataSheet, 'Metadata');
        }

        // Generate Excel file
        const filename = options.filename || `chart_data_${Date.now()}.xlsx`;
        XLSX.writeFile(workbook, filename);

        return workbook;
    }

    /**
     * Create metadata worksheet for Excel export
     */
    createMetadataSheet(chart, options) {
        const metadata = [
            ['Export Information'],
            ['Generated Date', new Date().toLocaleDateString()],
            ['Generated Time', new Date().toLocaleTimeString()],
            ['Chart Type', chart.config.type],
            ['Total Data Points', chart.data.datasets.reduce((sum, ds) => sum + ds.data.length, 0)],
            ['Number of Datasets', chart.data.datasets.length],
            [''],
            ['Chart Configuration'],
            ['Title', options.title || 'Chart Export'],
            ['Data Source', 'Interactive Demo'],
            [''],
            ['Generated by Brian Hardin Interactive Demos']
        ];

        const worksheet = XLSX.utils.aoa_to_sheet(metadata);

        // Style the header
        if (worksheet['A1']) {
            worksheet['A1'].s = {
                font: { bold: true, sz: 14 },
                fill: { fgColor: { rgb: 'DDDDDD' } }
            };
        }

        return worksheet;
    }

    /**
     * Dynamically load external scripts
     */
    async loadScript(src) {
        return new Promise((resolve, reject) => {
            // Check if script is already loaded
            if (document.querySelector(`script[src="${src}"]`)) {
                resolve();
                return;
            }

            const script = document.createElement('script');
            script.src = src;
            script.onload = resolve;
            script.onerror = reject;
            document.head.appendChild(script);
        });
    }

    /**
     * Show loading state for chart
     */
    showChartLoading(chartId) {
        const chart = this.charts.get(chartId);
        const container = chart.canvas.parentElement;

        // Add loading overlay
        const loadingOverlay = document.createElement('div');
        loadingOverlay.className = 'chart-loading-overlay';
        loadingOverlay.innerHTML = `
            <div class="loading-spinner">
                <svg class="animate-spin h-8 w-8" fill="none" viewBox="0 0 24 24">
                    <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                    <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                </svg>
                <span>Loading...</span>
            </div>
        `;

        container.appendChild(loadingOverlay);
    }

    /**
     * Hide loading state
     */
    hideChartLoading(chartId) {
        const chart = this.charts.get(chartId);
        const container = chart.canvas.parentElement;
        const overlay = container.querySelector('.chart-loading-overlay');

        if (overlay) {
            container.removeChild(overlay);
        }
    }

    /**
     * Show chart error
     */
    showChartError(chartId, message) {
        this.hideChartLoading(chartId);

        const chart = this.charts.get(chartId);
        const container = chart.canvas.parentElement;

        const errorOverlay = document.createElement('div');
        errorOverlay.className = 'chart-error-overlay';
        errorOverlay.innerHTML = `
            <div class="error-message">
                <svg class="h-8 w-8 text-red-500" fill="none" viewBox="0 0 24 24">
                    <path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/>
                </svg>
                <span>${message}</span>
                <button onclick="this.parentElement.parentElement.remove()" class="retry-btn">Dismiss</button>
            </div>
        `;

        container.appendChild(errorOverlay);

        // Auto-remove after 5 seconds
        setTimeout(() => {
            if (errorOverlay.parentElement) {
                errorOverlay.parentElement.removeChild(errorOverlay);
            }
        }, 5000);
    }

    /**
     * Add back button for drill-down
     */
    addBackButton(chartId) {
        const chart = this.charts.get(chartId);
        const container = chart.canvas.parentElement;

        // Remove existing back button
        this.removeBackButton(chartId);

        const backButton = document.createElement('button');
        backButton.className = 'chart-back-button';
        backButton.innerHTML = '← Back';
        backButton.onclick = () => this.drillUp(chartId);

        container.appendChild(backButton);
    }

    /**
     * Remove back button
     */
    removeBackButton(chartId) {
        const chart = this.charts.get(chartId);
        const container = chart.canvas.parentElement;
        const backButton = container.querySelector('.chart-back-button');

        if (backButton) {
            container.removeChild(backButton);
        }
    }

    /**
     * Trigger custom chart events
     */
    triggerChartEvent(chartId, eventType, data) {
        const event = new CustomEvent(`chart:${eventType}`, {
            detail: { chartId, ...data }
        });
        document.dispatchEvent(event);
    }

    /**
     * Export queue management
     */
    addToExportQueue(chartId, format) {
        this.exportQueue.push({ chartId, format, timestamp: Date.now() });

        // Show export indicator
        const chart = this.charts.get(chartId);
        const container = chart.canvas.parentElement;

        let indicator = container.querySelector('.export-indicator');
        if (!indicator) {
            indicator = document.createElement('div');
            indicator.className = 'export-indicator';
            indicator.innerHTML = `Exporting as ${format.toUpperCase()}...`;
            container.appendChild(indicator);
        }
    }

    removeFromExportQueue(chartId, format) {
        this.exportQueue = this.exportQueue.filter(
            item => !(item.chartId === chartId && item.format === format)
        );

        // Hide export indicator if no more exports for this chart
        const hasActiveExports = this.exportQueue.some(item => item.chartId === chartId);
        if (!hasActiveExports) {
            const chart = this.charts.get(chartId);
            const container = chart.canvas.parentElement;
            const indicator = container.querySelector('.export-indicator');

            if (indicator) {
                container.removeChild(indicator);
            }
        }
    }

    /**
     * Get chart statistics
     */
    getChartStats(chartId) {
        const chart = this.charts.get(chartId);
        const stack = this.drillDownStacks.get(chartId);
        const filters = this.filters.get(chartId);

        return {
            totalDataPoints: chart.data.datasets.reduce((sum, ds) => sum + ds.data.length, 0),
            drillDownLevel: stack.length,
            activeFilters: Object.keys(filters).length,
            chartType: chart.config.type,
            lastUpdated: chart.lastUpdate || Date.now()
        };
    }

    /**
     * Export chart with advanced options
     */
    async exportChartAdvanced(chartId, format, advancedOptions = {}) {
        const defaultOptions = {
            includeData: true,
            includeMetadata: true,
            title: `Chart Export - ${new Date().toLocaleDateString()}`,
            orientation: 'landscape',
            format: 'a4',
            quality: 0.9
        };

        const options = { ...defaultOptions, ...advancedOptions };
        return await this.exportChart(chartId, format, options);
    }

    /**
     * Export all charts in a dashboard
     */
    async exportDashboard(dashboardCharts, format = 'pdf', options = {}) {
        if (format === 'pdf') {
            return await this.exportDashboardAsPDF(dashboardCharts, options);
        } else {
            // Export individual charts
            const exports = [];
            for (const chartId of dashboardCharts) {
                try {
                    const result = await this.exportChart(chartId, format, options);
                    exports.push({ chartId, result, success: true });
                } catch (error) {
                    exports.push({ chartId, error: error.message, success: false });
                }
            }
            return exports;
        }
    }

    /**
     * Export multiple charts to single PDF
     */
    async exportDashboardAsPDF(chartIds, options = {}) {
        if (!window.jsPDF) {
            await this.loadScript('https://cdnjs.cloudflare.com/ajax/libs/jspdf/2.5.1/jspdf.umd.min.js');
        }

        const { jsPDF } = window;
        const pdf = new jsPDF({
            orientation: options.orientation || 'landscape',
            unit: 'mm',
            format: options.format || 'a4'
        });

        const pageWidth = pdf.internal.pageSize.getWidth();
        const pageHeight = pdf.internal.pageSize.getHeight();
        const margin = 20;

        // Title page
        pdf.setFontSize(20);
        pdf.setFont(undefined, 'bold');
        pdf.text(options.dashboardTitle || 'Dashboard Export', margin, margin + 10);

        pdf.setFontSize(12);
        pdf.setFont(undefined, 'normal');
        pdf.text(`Generated on ${new Date().toLocaleDateString()} at ${new Date().toLocaleTimeString()}`, margin, margin + 25);
        pdf.text(`Contains ${chartIds.length} charts`, margin, margin + 35);

        // Add each chart on separate page
        for (let i = 0; i < chartIds.length; i++) {
            const chartId = chartIds[i];
            const chart = this.charts.get(chartId);

            if (!chart) continue;

            // Add new page for each chart (except first)
            if (i > 0) {
                pdf.addPage();
            } else {
                // Move to next section on title page
                pdf.addPage();
            }

            // Chart title
            pdf.setFontSize(16);
            pdf.setFont(undefined, 'bold');
            const chartTitle = options.chartTitles?.[chartId] || `Chart ${i + 1}`;
            pdf.text(chartTitle, margin, margin);

            // Add chart image
            const canvas = chart.canvas;
            const imgData = canvas.toDataURL('image/png', 0.9);

            const maxWidth = pageWidth - (margin * 2);
            const maxHeight = (pageHeight - (margin * 3)) * 0.7; // Leave space for data

            const imgAspectRatio = canvas.width / canvas.height;
            let imgWidth = maxWidth;
            let imgHeight = imgWidth / imgAspectRatio;

            if (imgHeight > maxHeight) {
                imgHeight = maxHeight;
                imgWidth = imgHeight * imgAspectRatio;
            }

            pdf.addImage(imgData, 'PNG', margin, margin + 15, imgWidth, imgHeight);

            // Add summary data
            if (options.includeData && chart.data) {
                const tableY = margin + 15 + imgHeight + 10;
                this.addDataTableToPDF(pdf, chart.data, margin, tableY, maxWidth);
            }
        }

        // Save dashboard PDF
        const filename = options.filename || `dashboard_export_${Date.now()}.pdf`;
        pdf.save(filename);

        return pdf;
    }
}

// CSS styles for chart overlays and indicators
const chartStyles = `
    .chart-loading-overlay,
    .chart-error-overlay {
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: rgba(255, 255, 255, 0.9);
        display: flex;
        align-items: center;
        justify-content: center;
        z-index: 1000;
    }

    .loading-spinner,
    .error-message {
        display: flex;
        flex-direction: column;
        align-items: center;
        gap: 0.5rem;
        text-align: center;
        padding: 1rem;
    }

    .chart-back-button {
        position: absolute;
        top: 10px;
        left: 10px;
        background: rgba(59, 130, 246, 0.9);
        color: white;
        border: none;
        padding: 0.5rem 1rem;
        border-radius: 0.375rem;
        cursor: pointer;
        font-size: 0.875rem;
        z-index: 100;
    }

    .chart-back-button:hover {
        background: rgba(59, 130, 246, 1);
    }

    .export-indicator {
        position: absolute;
        top: 10px;
        right: 10px;
        background: rgba(34, 197, 94, 0.9);
        color: white;
        padding: 0.25rem 0.75rem;
        border-radius: 0.375rem;
        font-size: 0.75rem;
        z-index: 100;
    }

    .retry-btn {
        background: #ef4444;
        color: white;
        border: none;
        padding: 0.25rem 0.75rem;
        border-radius: 0.25rem;
        cursor: pointer;
        font-size: 0.75rem;
        margin-top: 0.5rem;
    }
`;

// Inject styles
if (!document.querySelector('#chart-utils-styles')) {
    const styleSheet = document.createElement('style');
    styleSheet.id = 'chart-utils-styles';
    styleSheet.textContent = chartStyles;
    document.head.appendChild(styleSheet);
}

// Global instance
window.advancedChartManager = new AdvancedChartManager();

// Export for module systems
if (typeof module !== 'undefined' && module.exports) {
    module.exports = AdvancedChartManager;
}
