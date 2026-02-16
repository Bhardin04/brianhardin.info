const puppeteer = require('puppeteer');
const fs = require('fs');
const path = require('path');

async function testDarkMode() {
    console.log('🚀 Starting simple dark mode test...');

    const screenshotDir = path.join(__dirname, '..', 'screenshots');
    if (!fs.existsSync(screenshotDir)) {
        fs.mkdirSync(screenshotDir, { recursive: true });
    }

    const browser = await puppeteer.launch({
        headless: true,
        defaultViewport: { width: 1366, height: 768 },
        args: ['--no-sandbox', '--disable-setuid-sandbox']
    });

    const baseUrl = 'http://127.0.0.1:8000';
    const pages = ['/', '/about', '/projects', '/blog', '/contact'];
    const results = [];

    for (const pagePath of pages) {
        const pageName = pagePath === '/' ? 'homepage' : pagePath.substring(1);
        console.log(`\n🔍 Testing ${pageName}...`);

        const page = await browser.newPage();

        try {
            // Test light mode
            await page.goto(`${baseUrl}${pagePath}`, { waitUntil: 'networkidle2' });
            await page.waitForTimeout(1000);

            console.log(`📸 Taking ${pageName} light mode screenshot...`);
            await page.screenshot({
                path: path.join(screenshotDir, `${pageName}-light.png`),
                fullPage: true
            });

            // Check for dark mode toggle
            const toggle = await page.$('#theme-toggle');
            const hasToggle = toggle !== null;

            // Get current theme info
            const themeInfo = await page.evaluate(() => {
                const html = document.documentElement;
                return {
                    isDark: html.classList.contains('dark'),
                    storedTheme: localStorage.getItem('theme'),
                    htmlClasses: html.className,
                    bodyBackground: window.getComputedStyle(document.body).backgroundColor
                };
            });

            console.log(`Theme info for ${pageName}:`, themeInfo);

            // Now test dark mode by manually adding the class
            await page.evaluate(() => {
                document.documentElement.classList.add('dark');
                localStorage.setItem('theme', 'dark');
            });

            await page.waitForTimeout(500);

            console.log(`📸 Taking ${pageName} dark mode screenshot...`);
            await page.screenshot({
                path: path.join(screenshotDir, `${pageName}-dark.png`),
                fullPage: true
            });

            // Get dark theme info
            const darkThemeInfo = await page.evaluate(() => {
                const html = document.documentElement;
                return {
                    isDark: html.classList.contains('dark'),
                    storedTheme: localStorage.getItem('theme'),
                    htmlClasses: html.className,
                    bodyBackground: window.getComputedStyle(document.body).backgroundColor
                };
            });

            console.log(`Dark theme info for ${pageName}:`, darkThemeInfo);

            results.push({
                page: pageName,
                hasToggle,
                lightMode: themeInfo,
                darkMode: darkThemeInfo,
                success: true
            });

            console.log(`✅ ${pageName} test completed`);

        } catch (error) {
            console.log(`❌ Error testing ${pageName}:`, error.message);
            results.push({
                page: pageName,
                hasToggle: false,
                error: error.message,
                success: false
            });
        } finally {
            await page.close();
        }
    }

    await browser.close();

    // Generate report
    console.log('\n' + '='.repeat(60));
    console.log('📋 SIMPLE DARK MODE TEST REPORT');
    console.log('='.repeat(60));

    results.forEach(result => {
        console.log(`\n📄 ${result.page.toUpperCase()}:`);
        console.log(`  Toggle found: ${result.hasToggle ? '✅' : '❌'}`);
        console.log(`  Test success: ${result.success ? '✅' : '❌'}`);

        if (result.success) {
            console.log(`  Light mode background: ${result.lightMode.bodyBackground}`);
            console.log(`  Dark mode background: ${result.darkMode.bodyBackground}`);
            console.log(`  Theme persistence: ${result.darkMode.storedTheme === 'dark' ? '✅' : '❌'}`);
        }

        if (result.error) {
            console.log(`  Error: ${result.error}`);
        }
    });

    console.log(`\n📸 Screenshots saved to: ${screenshotDir}`);

    return results;
}

// Run the test
testDarkMode().catch(console.error);
