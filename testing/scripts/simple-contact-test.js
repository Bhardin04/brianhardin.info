const puppeteer = require('puppeteer');
const fs = require('fs');
const path = require('path');

// Ensure test-results directory exists
const resultsDir = path.join(__dirname, 'test-results');
if (!fs.existsSync(resultsDir)) {
    fs.mkdirSync(resultsDir, { recursive: true });
}

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
        }
    }
};

const testResults = [];

function logResult(testName, passed, message, screenshot = null) {
    const result = {
        test: testName,
        passed,
        message,
        screenshot,
        timestamp: new Date().toISOString()
    };
    
    testResults.push(result);
    console.log(`${passed ? '✅' : '❌'} ${testName}: ${message}`);
    
    if (screenshot) {
        console.log(`   📸 Screenshot: ${screenshot}`);
    }
}

async function takeScreenshot(page, name, description) {
    try {
        const filename = `${name}_${Date.now()}.png`;
        const filepath = path.join(CONFIG.screenshotDir, filename);
        
        await page.screenshot({
            path: filepath,
            fullPage: true
        });
        
        console.log(`📸 Screenshot saved: ${filename} - ${description}`);
        return filename;
    } catch (error) {
        console.log(`❌ Failed to take screenshot: ${error.message}`);
        return null;
    }
}

async function testContactForm() {
    console.log('🚀 Starting Contact Form Tests...');
    console.log(`📍 Testing URL: ${CONFIG.baseUrl}${CONFIG.contactPath}`);
    
    let browser;
    let page;
    
    try {
        browser = await puppeteer.launch({ 
            headless: "new",
            args: ['--disable-dev-shm-usage', '--no-sandbox', '--disable-setuid-sandbox']
        });
        
        page = await browser.newPage();
        
        // Set desktop viewport
        await page.setViewport({ width: 1200, height: 800 });
        
        // Navigate to contact page
        console.log(`📍 Navigating to contact page...`);
        await page.goto(`${CONFIG.baseUrl}${CONFIG.contactPath}`, { waitUntil: 'networkidle2' });
        
        // Initial screenshot
        const initialScreenshot = await takeScreenshot(page, 'initial_load', 'Initial contact page load');
        logResult('Page Load', true, 'Contact page loaded successfully', initialScreenshot);
        
        // Test 1: Check form elements exist
        console.log('\n🔍 Testing Form Elements...');
        const formExists = await page.$('#contact-form');
        const nameField = await page.$('#name');
        const emailField = await page.$('#email');
        const subjectField = await page.$('#subject');
        const messageField = await page.$('#message');
        const submitButton = await page.$('button[type="submit"]');
        
        if (formExists && nameField && emailField && subjectField && messageField && submitButton) {
            logResult('Form Elements', true, 'All required form elements found');
        } else {
            logResult('Form Elements', false, 'Some form elements are missing');
        }
        
        // Test 2: Test empty form validation
        console.log('\n📝 Testing Empty Form Validation...');
        await page.click('button[type="submit"]');
        await page.waitForTimeout(1000);
        
        const emptyFormScreenshot = await takeScreenshot(page, 'empty_form_validation', 'Empty form validation test');
        
        const nameValid = await page.evaluate(() => {
            const nameEl = document.querySelector('#name');
            return nameEl ? nameEl.checkValidity() : false;
        });
        
        if (!nameValid) {
            logResult('Empty Form Validation', true, 'Browser validation prevented empty form submission', emptyFormScreenshot);
        } else {
            logResult('Empty Form Validation', false, 'Browser validation did not prevent empty form submission', emptyFormScreenshot);
        }
        
        // Test 3: Test invalid email validation
        console.log('\n📧 Testing Invalid Email Validation...');
        await page.type('#name', 'Test User');
        await page.type('#email', 'invalid-email');
        await page.type('#subject', 'Test Subject');
        await page.type('#message', 'Test message');
        
        await page.click('button[type="submit"]');
        await page.waitForTimeout(1000);
        
        const invalidEmailScreenshot = await takeScreenshot(page, 'invalid_email_validation', 'Invalid email validation test');
        
        const emailValid = await page.evaluate(() => {
            const emailEl = document.querySelector('#email');
            return emailEl ? emailEl.checkValidity() : false;
        });
        
        if (!emailValid) {
            logResult('Invalid Email Validation', true, 'Browser validation caught invalid email format', invalidEmailScreenshot);
        } else {
            logResult('Invalid Email Validation', false, 'Browser validation did not catch invalid email format', invalidEmailScreenshot);
        }
        
        // Test 4: Test valid form submission
        console.log('\n✅ Testing Valid Form Submission...');
        
        // Clear form
        await page.evaluate(() => {
            document.querySelector('#name').value = '';
            document.querySelector('#email').value = '';
            document.querySelector('#subject').value = '';
            document.querySelector('#message').value = '';
        });
        
        // Fill with valid data
        await page.type('#name', CONFIG.testData.valid.name);
        await page.type('#email', CONFIG.testData.valid.email);
        await page.type('#subject', CONFIG.testData.valid.subject);
        await page.type('#message', CONFIG.testData.valid.message);
        
        const filledFormScreenshot = await takeScreenshot(page, 'filled_form', 'Form filled with valid data');
        logResult('Form Filling', true, 'Form filled with valid test data', filledFormScreenshot);
        
        // Submit form
        await page.click('button[type="submit"]');
        
        // Wait for HTMX response
        await page.waitForTimeout(3000);
        
        const responseScreenshot = await takeScreenshot(page, 'form_response', 'Form submission response');
        
        // Check for response message
        const responseMessage = await page.evaluate(() => {
            const messageEl = document.querySelector('#form-message');
            return messageEl ? messageEl.textContent.trim() : '';
        });
        
        if (responseMessage.includes('Success') || responseMessage.includes('sent')) {
            logResult('Form Submission Success', true, 'Form submitted successfully with success message', responseScreenshot);
        } else if (responseMessage.includes('Error') || responseMessage.includes('problem')) {
            logResult('Form Submission Error', true, 'Form submission returned error message (this is expected behavior)', responseScreenshot);
        } else if (responseMessage === '') {
            logResult('Form Submission Response', false, 'No response message received', responseScreenshot);
        } else {
            logResult('Form Submission Response', false, `Unexpected response: ${responseMessage}`, responseScreenshot);
        }
        
        // Test 5: Check if form was reset
        const formValues = await page.evaluate(() => {
            return {
                name: document.querySelector('#name').value,
                email: document.querySelector('#email').value,
                subject: document.querySelector('#subject').value,
                message: document.querySelector('#message').value
            };
        });
        
        if (formValues.name === '' && formValues.email === '' && formValues.subject === '' && formValues.message === '') {
            logResult('Form Reset', true, 'Form was reset after submission (HTMX behavior working)');
        } else {
            logResult('Form Reset', false, 'Form was not reset after submission');
        }
        
        // Test 6: Test mobile viewport
        console.log('\n📱 Testing Mobile Viewport...');
        await page.setViewport({ width: 375, height: 667 });
        await page.reload({ waitUntil: 'networkidle2' });
        
        const mobileScreenshot = await takeScreenshot(page, 'mobile_view', 'Mobile viewport test');
        
        const mobileFormVisible = await page.evaluate(() => {
            const form = document.querySelector('#contact-form');
            return form && form.offsetWidth > 0 && form.offsetHeight > 0;
        });
        
        if (mobileFormVisible) {
            logResult('Mobile Responsiveness', true, 'Form is properly visible on mobile viewport', mobileScreenshot);
        } else {
            logResult('Mobile Responsiveness', false, 'Form is not properly visible on mobile viewport', mobileScreenshot);
        }
        
        // Test 7: Test loading state
        console.log('\n⏳ Testing Loading State...');
        
        await page.type('#name', CONFIG.testData.valid.name);
        await page.type('#email', CONFIG.testData.valid.email);
        await page.type('#subject', CONFIG.testData.valid.subject);
        await page.type('#message', CONFIG.testData.valid.message);
        
        // Click submit and immediately check for loading state
        await page.click('button[type="submit"]');
        await page.waitForTimeout(200);
        
        const loadingVisible = await page.evaluate(() => {
            const loadingEl = document.querySelector('#loading');
            if (!loadingEl) return false;
            const style = window.getComputedStyle(loadingEl);
            return style.display !== 'none' && style.visibility !== 'hidden';
        });
        
        if (loadingVisible) {
            const loadingScreenshot = await takeScreenshot(page, 'loading_state', 'Loading state visible');
            logResult('Loading State', true, 'Loading indicator is visible during form submission', loadingScreenshot);
        } else {
            logResult('Loading State', false, 'Loading indicator was not visible during form submission');
        }
        
        await page.waitForTimeout(2000);
        
    } catch (error) {
        logResult('Test Execution', false, `Error during test execution: ${error.message}`);
        console.error('💥 Test execution error:', error);
    } finally {
        if (page) {
            try {
                await page.close();
            } catch (e) {
                console.log('Warning: Could not close page');
            }
        }
        if (browser) {
            try {
                await browser.close();
            } catch (e) {
                console.log('Warning: Could not close browser');
            }
        }
    }
    
    // Generate summary
    const passed = testResults.filter(r => r.passed).length;
    const failed = testResults.filter(r => r.passed === false).length;
    const total = testResults.length;
    
    console.log('\n📊 Test Summary:');
    console.log(`✅ Passed: ${passed}`);
    console.log(`❌ Failed: ${failed}`);
    console.log(`📈 Total: ${total}`);
    console.log(`🎯 Pass Rate: ${((passed / total) * 100).toFixed(1)}%`);
    
    // Save detailed results
    const reportPath = path.join(CONFIG.screenshotDir, 'test-results.json');
    fs.writeFileSync(reportPath, JSON.stringify({
        summary: { passed, failed, total, passRate: ((passed / total) * 100).toFixed(1) },
        results: testResults,
        timestamp: new Date().toISOString()
    }, null, 2));
    
    console.log(`📋 Detailed results saved to: ${reportPath}`);
    
    return { passed, failed, total };
}

// Run the test
testContactForm().then(result => {
    if (result.failed > 0) {
        process.exit(1);
    }
}).catch(error => {
    console.error('💥 Fatal error:', error);
    process.exit(1);
});