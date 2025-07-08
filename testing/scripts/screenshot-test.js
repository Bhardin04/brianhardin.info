const puppeteer = require('puppeteer');
const fs = require('fs');
const path = require('path');

// Simple screenshot test that works around browser connection issues
async function takeScreenshots() {
    const resultsDir = path.join(__dirname, 'test-results');
    if (!fs.existsSync(resultsDir)) {
        fs.mkdirSync(resultsDir, { recursive: true });
    }

    let browser;
    try {
        console.log('🚀 Starting screenshot capture...');
        
        browser = await puppeteer.launch({ 
            headless: "new",
            args: ['--no-sandbox', '--disable-setuid-sandbox', '--disable-dev-shm-usage']
        });

        const page = await browser.newPage();
        
        // Desktop view
        await page.setViewport({ width: 1200, height: 800 });
        await page.goto('http://127.0.0.1:8000/contact', { waitUntil: 'networkidle2' });
        
        await page.screenshot({
            path: path.join(resultsDir, 'contact-desktop.png'),
            fullPage: true
        });
        console.log('✅ Desktop screenshot saved');
        
        // Mobile view
        await page.setViewport({ width: 375, height: 667 });
        await page.reload({ waitUntil: 'networkidle2' });
        
        await page.screenshot({
            path: path.join(resultsDir, 'contact-mobile.png'),
            fullPage: true
        });
        console.log('✅ Mobile screenshot saved');
        
        await browser.close();
        console.log('🎉 Screenshots completed successfully!');
        
    } catch (error) {
        console.error('❌ Screenshot error:', error.message);
        if (browser) {
            await browser.close();
        }
    }
}

takeScreenshots();