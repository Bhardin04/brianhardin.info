const puppeteer = require('puppeteer');
const fs = require('fs');
const path = require('path');

/**
 * Sales Dashboard Test Script
 * Tests the functionality and performance of the sales dashboard demo
 */

async function testSalesDashboard() {
    const browser = await puppeteer.launch({
        headless: true, // Use headless for better stability
        defaultViewport: { width: 1200, height: 800 },
        args: [
            '--no-sandbox',
            '--disable-setuid-sandbox',
            '--disable-web-security',
            '--disable-features=VizDisplayCompositor'
        ]
    });

    const page = await browser.newPage();
    const results = {
        timestamp: new Date().toISOString(),
        testName: 'Sales Dashboard Test',
        url: 'http://localhost:8000/demos/sales-dashboard',
        tests: [],
        summary: {
            passed: 0,
            failed: 0,
            warnings: 0
        }
    };

    // Track console messages and errors
    const consoleMessages = [];
    const errors = [];

    page.on('console', msg => {
        consoleMessages.push({
            type: msg.type(),
            text: msg.text(),
            timestamp: new Date().toISOString()
        });
    });

    page.on('pageerror', error => {
        errors.push({
            message: error.message,
            stack: error.stack,
            timestamp: new Date().toISOString()
        });
    });

    try {
        console.log('🚀 Starting Sales Dashboard Tests...');

        // Test 1: Page loads successfully
        console.log('📄 Testing page load...');
        await page.goto('http://localhost:8000/demos/sales-dashboard', {
            waitUntil: 'networkidle2',
            timeout: 30000
        });

        results.tests.push({
            name: 'Page Load',
            status: 'PASSED',
            message: 'Dashboard page loaded successfully',
            duration: 0
        });
        results.summary.passed++;

        // Test 2: Check for critical JavaScript errors
        console.log('🔍 Checking for JavaScript errors...');
        await page.waitForTimeout(3000); // Wait for JS to execute

        const criticalErrors = errors.filter(err =>
            err.message.includes('ReferenceError') ||
            err.message.includes('TypeError') ||
            err.message.includes('SyntaxError')
        );

        if (criticalErrors.length === 0) {
            results.tests.push({
                name: 'JavaScript Errors',
                status: 'PASSED',
                message: 'No critical JavaScript errors found',
                duration: 0
            });
            results.summary.passed++;
        } else {
            results.tests.push({
                name: 'JavaScript Errors',
                status: 'FAILED',
                message: `Found ${criticalErrors.length} critical JavaScript errors`,
                details: criticalErrors,
                duration: 0
            });
            results.summary.failed++;
        }

        // Test 3: Check if session status initializes
        console.log('🔗 Testing session initialization...');
        const sessionStatus = await page.$('#session-status');
        if (sessionStatus) {
            const statusText = await page.evaluate(el => el.textContent, sessionStatus);

            if (statusText.includes('Initializing') || statusText.includes('Connected')) {
                results.tests.push({
                    name: 'Session Status',
                    status: 'PASSED',
                    message: `Session status: ${statusText.trim()}`,
                    duration: 0
                });
                results.summary.passed++;
            } else {
                results.tests.push({
                    name: 'Session Status',
                    status: 'FAILED',
                    message: `Unexpected session status: ${statusText}`,
                    duration: 0
                });
                results.summary.failed++;
            }
        } else {
            results.tests.push({
                name: 'Session Status',
                status: 'FAILED',
                message: 'Session status element not found',
                duration: 0
            });
            results.summary.failed++;
        }

        // Test 4: Check for dashboard elements
        console.log('📊 Testing dashboard elements...');
        const elements = [
            { selector: '#kpi-section', name: 'KPI Section' },
            { selector: '#revenue-chart', name: 'Revenue Chart' },
            { selector: '#customer-chart', name: 'Customer Chart' },
            { selector: '#revenue-table', name: 'Revenue Table' },
            { selector: '#margin-chart', name: 'Margin Chart' }
        ];

        for (const element of elements) {
            const exists = await page.$(element.selector) !== null;
            if (exists) {
                results.tests.push({
                    name: `Element: ${element.name}`,
                    status: 'PASSED',
                    message: `${element.name} element found`,
                    duration: 0
                });
                results.summary.passed++;
            } else {
                results.tests.push({
                    name: `Element: ${element.name}`,
                    status: 'FAILED',
                    message: `${element.name} element not found`,
                    duration: 0
                });
                results.summary.failed++;
            }
        }

        // Test 5: Test button interactions
        console.log('🎯 Testing button interactions...');
        try {
            await page.click('#refresh-btn');
            await page.waitForTimeout(2000);

            results.tests.push({
                name: 'Refresh Button',
                status: 'PASSED',
                message: 'Refresh button clicked successfully',
                duration: 0
            });
            results.summary.passed++;
        } catch (error) {
            results.tests.push({
                name: 'Refresh Button',
                status: 'FAILED',
                message: `Refresh button interaction failed: ${error.message}`,
                duration: 0
            });
            results.summary.failed++;
        }

        // Test 6: Check for chart canvases (Chart.js elements)
        console.log('📈 Testing chart rendering...');
        await page.waitForTimeout(5000); // Wait for charts to load

        const chartCanvases = await page.$$('canvas');
        if (chartCanvases.length > 0) {
            results.tests.push({
                name: 'Chart Canvases',
                status: 'PASSED',
                message: `Found ${chartCanvases.length} chart canvas elements`,
                duration: 0
            });
            results.summary.passed++;
        } else {
            results.tests.push({
                name: 'Chart Canvases',
                status: 'WARNING',
                message: 'No chart canvas elements found - charts may not be rendering',
                duration: 0
            });
            results.summary.warnings++;
        }

        // Test 7: Performance check
        console.log('⚡ Testing performance...');
        const performanceMetrics = await page.evaluate(() => {
            const navigation = performance.getEntriesByType('navigation')[0];
            return {
                loadTime: navigation.loadEventEnd - navigation.loadEventStart,
                domContentLoaded: navigation.domContentLoadedEventEnd - navigation.domContentLoadedEventStart,
                totalTime: navigation.loadEventEnd - navigation.fetchStart
            };
        });

        if (performanceMetrics.totalTime < 5000) {
            results.tests.push({
                name: 'Page Performance',
                status: 'PASSED',
                message: `Page loaded in ${performanceMetrics.totalTime.toFixed(2)}ms`,
                details: performanceMetrics,
                duration: 0
            });
            results.summary.passed++;
        } else {
            results.tests.push({
                name: 'Page Performance',
                status: 'WARNING',
                message: `Page took ${performanceMetrics.totalTime.toFixed(2)}ms to load (>5s)`,
                details: performanceMetrics,
                duration: 0
            });
            results.summary.warnings++;
        }

        // Test 8: Check for memory leaks (basic)
        console.log('🧠 Testing memory usage...');
        const memoryInfo = await page.evaluate(() => {
            if (performance.memory) {
                return {
                    used: performance.memory.usedJSHeapSize,
                    total: performance.memory.totalJSHeapSize,
                    limit: performance.memory.jsHeapSizeLimit,
                    usagePercentage: (performance.memory.usedJSHeapSize / performance.memory.jsHeapSizeLimit) * 100
                };
            }
            return null;
        });

        if (memoryInfo) {
            if (memoryInfo.usagePercentage < 10) {
                results.tests.push({
                    name: 'Memory Usage',
                    status: 'PASSED',
                    message: `Memory usage: ${memoryInfo.usagePercentage.toFixed(2)}%`,
                    details: memoryInfo,
                    duration: 0
                });
                results.summary.passed++;
            } else {
                results.tests.push({
                    name: 'Memory Usage',
                    status: 'WARNING',
                    message: `High memory usage: ${memoryInfo.usagePercentage.toFixed(2)}%`,
                    details: memoryInfo,
                    duration: 0
                });
                results.summary.warnings++;
            }
        } else {
            results.tests.push({
                name: 'Memory Usage',
                status: 'SKIPPED',
                message: 'Memory API not available',
                duration: 0
            });
        }

        // Take a screenshot
        console.log('📸 Taking screenshot...');
        const screenshotPath = path.join(__dirname, '../reports/sales-dashboard-screenshot.png');
        await page.screenshot({
            path: screenshotPath,
            fullPage: true
        });

        results.screenshotPath = screenshotPath;

    } catch (error) {
        console.error('❌ Test failed:', error);
        results.tests.push({
            name: 'Test Execution',
            status: 'FAILED',
            message: `Test execution failed: ${error.message}`,
            duration: 0
        });
        results.summary.failed++;
    } finally {
        // Add console messages and errors to results
        results.consoleMessages = consoleMessages;
        results.errors = errors;

        await browser.close();
    }

    // Save results
    const reportPath = path.join(__dirname, '../reports/sales-dashboard-test-results.json');
    fs.writeFileSync(reportPath, JSON.stringify(results, null, 2));

    // Print summary
    console.log('\n📊 Test Summary:');
    console.log(`✅ Passed: ${results.summary.passed}`);
    console.log(`❌ Failed: ${results.summary.failed}`);
    console.log(`⚠️  Warnings: ${results.summary.warnings}`);
    console.log(`📁 Report saved to: ${reportPath}`);

    if (results.screenshotPath) {
        console.log(`📸 Screenshot saved to: ${results.screenshotPath}`);
    }

    return results;
}

// Run the test
if (require.main === module) {
    testSalesDashboard()
        .then(results => {
            console.log('\n🎉 Sales Dashboard test completed!');
            process.exit(results.summary.failed > 0 ? 1 : 0);
        })
        .catch(error => {
            console.error('💥 Test runner failed:', error);
            process.exit(1);
        });
}

module.exports = testSalesDashboard;
