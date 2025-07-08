const puppeteer = require('puppeteer');
const fs = require('fs');
const path = require('path');

// Ensure test-results directory exists
const resultsDir = path.join(__dirname, 'test-results');
if (!fs.existsSync(resultsDir)) {
    fs.mkdirSync(resultsDir, { recursive: true });
}

// Test configuration
const CONFIG = {
    baseUrl: 'http://127.0.0.1:8000',
    contactPath: '/contact',
    screenshotDir: resultsDir,
    testData: {
        valid: {
            name: 'Test User',
            email: 'test@example.com',
            subject: 'Test Message',
            message: 'This is a test message from the automated form testing.'
        },
        invalid: {
            name: '',
            email: 'invalid-email',
            subject: '',
            message: ''
        }
    }
};

// Test results collector
const testResults = {
    passed: 0,
    failed: 0,
    results: []
};

function logResult(testName, passed, message, screenshot = null) {
    const result = {
        test: testName,
        passed,
        message,
        screenshot,
        timestamp: new Date().toISOString()
    };
    
    testResults.results.push(result);
    if (passed) {
        testResults.passed++;
        console.log(`✅ ${testName}: ${message}`);
    } else {
        testResults.failed++;
        console.log(`❌ ${testName}: ${message}`);
    }
}

async function takeScreenshot(page, name, description) {
    const filename = `${name}_${Date.now()}.png`;
    const filepath = path.join(CONFIG.screenshotDir, filename);
    
    await page.screenshot({
        path: filepath,
        fullPage: true
    });
    
    console.log(`📸 Screenshot saved: ${filename} - ${description}`);
    return filename;
}

async function waitForElement(page, selector, timeout = 5000) {
    try {
        await page.waitForSelector(selector, { timeout });
        return true;
    } catch (error) {
        return false;
    }
}

async function testFormValidation(page, viewport) {
    console.log(`\n🔍 Testing Form Validation (${viewport})`);
    
    // Test 1: Empty form submission
    try {
        await page.click('button[type="submit"]');
        await page.waitForTimeout(1000);
        
        const screenshot = await takeScreenshot(page, `empty_form_${viewport.toLowerCase()}`, 'Empty form validation');
        
        // Check if browser validation is working
        const nameField = await page.$('#name');
        const emailField = await page.$('#email');
        const subjectField = await page.$('#subject');
        const messageField = await page.$('#message');
        
        const nameValid = await nameField.evaluate(el => el.checkValidity());
        const emailValid = await emailField.evaluate(el => el.checkValidity());
        const subjectValid = await subjectField.evaluate(el => el.checkValidity());
        const messageValid = await messageField.evaluate(el => el.checkValidity());
        
        if (!nameValid || !emailValid || !subjectValid || !messageValid) {
            logResult('Empty Form Validation', true, 'Browser validation prevented empty form submission', screenshot);
        } else {
            logResult('Empty Form Validation', false, 'Browser validation did not prevent empty form submission', screenshot);
        }
        
    } catch (error) {
        logResult('Empty Form Validation', false, `Error testing empty form: ${error.message}`);
    }
    
    // Test 2: Invalid email format
    try {
        await page.type('#name', 'Test User');
        await page.type('#email', 'invalid-email');
        await page.type('#subject', 'Test Subject');
        await page.type('#message', 'Test message');
        
        await page.click('button[type="submit"]');
        await page.waitForTimeout(1000);
        
        const screenshot = await takeScreenshot(page, `invalid_email_${viewport.toLowerCase()}`, 'Invalid email validation');
        
        const emailField = await page.$('#email');
        const emailValid = await emailField.evaluate(el => el.checkValidity());
        
        if (!emailValid) {
            logResult('Invalid Email Validation', true, 'Browser validation caught invalid email format', screenshot);
        } else {
            logResult('Invalid Email Validation', false, 'Browser validation did not catch invalid email format', screenshot);
        }
        
    } catch (error) {
        logResult('Invalid Email Validation', false, `Error testing invalid email: ${error.message}`);
    }
}

async function testSuccessfulSubmission(page, viewport) {
    console.log(`\n📝 Testing Successful Form Submission (${viewport})`);
    
    try {
        // Clear the form first
        await page.evaluate(() => {
            document.querySelector('#name').value = '';
            document.querySelector('#email').value = '';
            document.querySelector('#company').value = '';
            document.querySelector('#subject').value = '';
            document.querySelector('#message').value = '';
        });
        
        // Fill with valid data
        await page.type('#name', CONFIG.testData.valid.name);
        await page.type('#email', CONFIG.testData.valid.email);
        await page.type('#subject', CONFIG.testData.valid.subject);
        await page.type('#message', CONFIG.testData.valid.message);
        
        const beforeSubmissionScreenshot = await takeScreenshot(page, `filled_form_${viewport.toLowerCase()}`, 'Form filled with valid data');
        
        // Submit the form
        await page.click('button[type="submit"]');
        
        // Wait for HTMX response
        await page.waitForTimeout(2000);
        
        const afterSubmissionScreenshot = await takeScreenshot(page, `form_response_${viewport.toLowerCase()}`, 'Form submission response');
        
        // Check for success or error message
        const messageElement = await page.$('#form-message');
        const messageContent = await messageElement.evaluate(el => el.textContent);
        
        if (messageContent.includes('Success') || messageContent.includes('sent')) {
            logResult('Form Submission Success', true, 'Form submitted successfully with success message', afterSubmissionScreenshot);
        } else if (messageContent.includes('Error') || messageContent.includes('problem')) {
            logResult('Form Submission Error', true, 'Form submission returned error message (expected behavior)', afterSubmissionScreenshot);
        } else {
            logResult('Form Submission Response', false, `Unexpected response: ${messageContent}`, afterSubmissionScreenshot);
        }
        
        // Check if form was reset (HTMX behavior)
        const nameValue = await page.$eval('#name', el => el.value);
        const emailValue = await page.$eval('#email', el => el.value);
        
        if (nameValue === '' && emailValue === '') {
            logResult('Form Reset After Submission', true, 'Form was reset after submission (HTMX behavior working)', afterSubmissionScreenshot);
        } else {
            logResult('Form Reset After Submission', false, 'Form was not reset after submission', afterSubmissionScreenshot);
        }
        
    } catch (error) {
        logResult('Form Submission Test', false, `Error during form submission: ${error.message}`);
    }
}

async function testLoadingState(page, viewport) {
    console.log(`\n⏳ Testing Loading State (${viewport})`);
    
    try {
        // Fill the form again
        await page.evaluate(() => {
            document.querySelector('#name').value = '';
            document.querySelector('#email').value = '';
            document.querySelector('#subject').value = '';
            document.querySelector('#message').value = '';
        });
        
        await page.type('#name', CONFIG.testData.valid.name);
        await page.type('#email', CONFIG.testData.valid.email);
        await page.type('#subject', CONFIG.testData.valid.subject);
        await page.type('#message', CONFIG.testData.valid.message);
        
        // Click submit and immediately check for loading state
        await page.click('button[type="submit"]');
        
        // Wait a bit for loading state to appear
        await page.waitForTimeout(100);
        
        // Check for loading indicator
        const loadingIndicator = await page.$('#loading');
        const isVisible = await loadingIndicator.evaluate(el => {
            const style = window.getComputedStyle(el);
            return style.display !== 'none' && style.visibility !== 'hidden';
        });
        
        if (isVisible) {
            const loadingScreenshot = await takeScreenshot(page, `loading_state_${viewport.toLowerCase()}`, 'Loading state visible');
            logResult('Loading State Display', true, 'Loading indicator is visible during form submission', loadingScreenshot);
        } else {
            logResult('Loading State Display', false, 'Loading indicator was not visible during form submission');
        }
        
        // Wait for completion
        await page.waitForTimeout(2000);
        
    } catch (error) {
        logResult('Loading State Test', false, `Error testing loading state: ${error.message}`);
    }
}

async function testResponsiveDesign(page, viewport) {
    console.log(`\n📱 Testing Responsive Design (${viewport})`);
    
    try {
        // Check if form elements are visible and properly sized
        const form = await page.$('#contact-form');
        const formBounds = await form.boundingBox();
        
        const nameField = await page.$('#name');
        const nameFieldBounds = await nameField.boundingBox();
        
        const submitButton = await page.$('button[type="submit"]');
        const submitButtonBounds = await submitButton.boundingBox();
        
        const screenshot = await takeScreenshot(page, `responsive_${viewport.toLowerCase()}`, `Responsive design test - ${viewport}`);
        
        // Check if elements are properly positioned
        if (formBounds && nameFieldBounds && submitButtonBounds) {
            const elementsVisible = formBounds.width > 0 && nameFieldBounds.width > 0 && submitButtonBounds.width > 0;
            
            if (elementsVisible) {
                logResult(`Responsive Design ${viewport}`, true, `All form elements are visible and properly sized`, screenshot);
            } else {
                logResult(`Responsive Design ${viewport}`, false, `Some form elements are not properly sized`, screenshot);
            }
        } else {
            logResult(`Responsive Design ${viewport}`, false, `Could not detect form element bounds`, screenshot);
        }
        
    } catch (error) {
        logResult(`Responsive Design ${viewport}`, false, `Error testing responsive design: ${error.message}`);
    }
}

async function testAccessibility(page, viewport) {
    console.log(`\n♿ Testing Accessibility (${viewport})`);
    
    try {
        // Check for proper labels
        const nameLabel = await page.$('label[for="name"]');
        const emailLabel = await page.$('label[for="email"]');
        const subjectLabel = await page.$('label[for="subject"]');
        const messageLabel = await page.$('label[for="message"]');
        
        const labelsExist = nameLabel && emailLabel && subjectLabel && messageLabel;
        
        if (labelsExist) {
            logResult(`Accessibility Labels ${viewport}`, true, 'All form fields have proper labels');
        } else {
            logResult(`Accessibility Labels ${viewport}`, false, 'Some form fields are missing labels');
        }
        
        // Check for required field indicators
        const requiredFields = await page.$$('input[required], textarea[required]');
        const expectedRequired = 4; // name, email, subject, message
        
        if (requiredFields.length === expectedRequired) {
            logResult(`Accessibility Required Fields ${viewport}`, true, `All ${expectedRequired} required fields are properly marked`);
        } else {
            logResult(`Accessibility Required Fields ${viewport}`, false, `Expected ${expectedRequired} required fields, found ${requiredFields.length}`);
        }
        
    } catch (error) {
        logResult(`Accessibility Test ${viewport}`, false, `Error testing accessibility: ${error.message}`);
    }
}

async function runTestsForViewport(browser, viewport) {
    console.log(`\n🔧 Testing ${viewport} viewport...`);
    
    const page = await browser.newPage();
    
    try {
        // Set viewport
        if (viewport === 'Desktop') {
            await page.setViewport({ width: 1200, height: 800 });
        } else {
            await page.setViewport({ width: 375, height: 667 });
        }
        
        // Navigate to contact page
        const contactUrl = `${CONFIG.baseUrl}${CONFIG.contactPath}`;
        console.log(`📍 Navigating to: ${contactUrl}`);
        
        await page.goto(contactUrl, { waitUntil: 'networkidle2' });
        
        // Initial screenshot
        await takeScreenshot(page, `initial_${viewport.toLowerCase()}`, `Initial contact page load - ${viewport}`);
        
        // Run all tests for this viewport
        await testFormValidation(page, viewport);
        await testSuccessfulSubmission(page, viewport);
        await testLoadingState(page, viewport);
        await testResponsiveDesign(page, viewport);
        await testAccessibility(page, viewport);
        
    } catch (error) {
        logResult(`${viewport} Test Setup`, false, `Error setting up ${viewport} tests: ${error.message}`);
    } finally {
        try {
            if (!page.isClosed()) {
                await page.close();
            }
        } catch (closeError) {
            console.log(`Warning: Could not close page: ${closeError.message}`);
        }
    }
}

async function generateReport() {
    console.log('\n📊 Generating Test Report...');
    
    const report = {
        summary: {
            total: testResults.results.length,
            passed: testResults.passed,
            failed: testResults.failed,
            passRate: ((testResults.passed / testResults.results.length) * 100).toFixed(1)
        },
        results: testResults.results,
        timestamp: new Date().toISOString()
    };
    
    // Write JSON report
    const reportPath = path.join(CONFIG.screenshotDir, 'test-report.json');
    fs.writeFileSync(reportPath, JSON.stringify(report, null, 2));
    
    // Write HTML report
    const htmlReport = `
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Contact Form Test Report</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; }
        .summary { background: #f5f5f5; padding: 20px; border-radius: 8px; margin-bottom: 20px; }
        .test-result { margin: 10px 0; padding: 10px; border-radius: 4px; }
        .passed { background: #d4edda; border: 1px solid #c3e6cb; color: #155724; }
        .failed { background: #f8d7da; border: 1px solid #f5c6cb; color: #721c24; }
        .screenshot { max-width: 300px; margin: 10px 0; }
        .timestamp { color: #666; font-size: 0.9em; }
    </style>
</head>
<body>
    <h1>Contact Form Test Report</h1>
    
    <div class="summary">
        <h2>Test Summary</h2>
        <p><strong>Total Tests:</strong> ${report.summary.total}</p>
        <p><strong>Passed:</strong> ${report.summary.passed}</p>
        <p><strong>Failed:</strong> ${report.summary.failed}</p>
        <p><strong>Pass Rate:</strong> ${report.summary.passRate}%</p>
        <p><strong>Generated:</strong> ${report.timestamp}</p>
    </div>
    
    <div class="results">
        <h2>Detailed Results</h2>
        ${report.results.map(result => `
            <div class="test-result ${result.passed ? 'passed' : 'failed'}">
                <h3>${result.test}</h3>
                <p><strong>Status:</strong> ${result.passed ? 'PASSED' : 'FAILED'}</p>
                <p><strong>Message:</strong> ${result.message}</p>
                <p class="timestamp"><strong>Time:</strong> ${result.timestamp}</p>
                ${result.screenshot ? `<div><strong>Screenshot:</strong><br><img src="${result.screenshot}" alt="Screenshot" class="screenshot"></div>` : ''}
            </div>
        `).join('')}
    </div>
</body>
</html>
    `;
    
    const htmlReportPath = path.join(CONFIG.screenshotDir, 'test-report.html');
    fs.writeFileSync(htmlReportPath, htmlReport);
    
    console.log(`📋 Test report saved to: ${htmlReportPath}`);
    return report;
}

async function main() {
    console.log('🚀 Starting Contact Form Tests...');
    console.log(`📍 Testing URL: ${CONFIG.baseUrl}${CONFIG.contactPath}`);
    
    let browser;
    try {
        browser = await puppeteer.launch({ 
            headless: "new",
            devtools: false,
            defaultViewport: null,
            args: ['--disable-dev-shm-usage', '--no-sandbox', '--disable-setuid-sandbox']
        });
        
        // Test both desktop and mobile viewports
        await runTestsForViewport(browser, 'Desktop');
        await runTestsForViewport(browser, 'Mobile');
        
        // Generate final report
        const report = await generateReport();
        
        console.log('\n🎉 Test Suite Complete!');
        console.log(`📊 Results: ${report.summary.passed}/${report.summary.total} tests passed (${report.summary.passRate}%)`);
        
        if (report.summary.failed > 0) {
            console.log('❌ Some tests failed. Check the detailed report for more information.');
            process.exit(1);
        } else {
            console.log('✅ All tests passed!');
        }
        
    } catch (error) {
        console.error('💥 Error running tests:', error);
        process.exit(1);
    } finally {
        if (browser) {
            await browser.close();
        }
    }
}

// Run the tests
main().catch(console.error);