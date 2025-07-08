const puppeteer = require('puppeteer');
const fs = require('fs');
const path = require('path');

class DarkModeTest {
    constructor() {
        this.browser = null;
        this.page = null;
        this.baseUrl = 'http://127.0.0.1:8000';
        this.screenshotDir = path.join(__dirname, '..', 'screenshots');
        this.testResults = {
            homepage: { light: null, dark: null },
            about: { light: null, dark: null },
            projects: { light: null, dark: null },
            blog: { light: null, dark: null },
            contact: { light: null, dark: null },
            localStorage: { persists: false, details: null },
            issues: []
        };
    }

    async initialize() {
        console.log('🚀 Initializing Dark Mode Test Suite...');
        
        // Ensure screenshots directory exists
        if (!fs.existsSync(this.screenshotDir)) {
            fs.mkdirSync(this.screenshotDir, { recursive: true });
        }

        this.browser = await puppeteer.launch({
            headless: true, // Run in headless mode for better stability
            defaultViewport: { width: 1366, height: 768 },
            args: [
                '--no-sandbox', 
                '--disable-setuid-sandbox',
                '--disable-dev-shm-usage',
                '--disable-gpu',
                '--disable-web-security',
                '--disable-features=VizDisplayCompositor'
            ]
        });

        this.page = await this.browser.newPage();
        
        // Set up console logging
        this.page.on('console', msg => {
            if (msg.type() === 'error') {
                console.log('🔴 Console Error:', msg.text());
                this.testResults.issues.push(`Console Error: ${msg.text()}`);
            }
        });

        // Set up error handling
        this.page.on('pageerror', error => {
            console.log('🔴 Page Error:', error.message);
            this.testResults.issues.push(`Page Error: ${error.message}`);
        });
    }

    async waitForDarkModeToggle() {
        try {
            await this.page.waitForSelector('[data-testid="dark-mode-toggle"], .dark-mode-toggle, #dark-mode-toggle, button[aria-label*="dark"], button[title*="dark"]', { timeout: 5000 });
            return true;
        } catch (error) {
            console.log('⚠️  Dark mode toggle not found with common selectors');
            return false;
        }
    }

    async findDarkModeToggleForPage(page) {
        // Try multiple selector strategies
        const selectors = [
            '[data-testid="dark-mode-toggle"]',
            '.dark-mode-toggle',
            '#dark-mode-toggle',
            'button[aria-label*="dark"]',
            'button[title*="dark"]',
            'button[class*="dark"]',
            'button[id*="dark"]',
            '.theme-toggle',
            '#theme-toggle',
            'button[aria-label*="theme"]',
            'button[title*="theme"]'
        ];

        for (const selector of selectors) {
            try {
                const element = await page.$(selector);
                if (element) {
                    console.log(`✅ Found dark mode toggle with selector: ${selector}`);
                    return element;
                }
            } catch (error) {
                // Continue to next selector
            }
        }

        // If no toggle found, try to find it by text content
        const textSelectors = [
            'button:has-text("Dark")',
            'button:has-text("Light")',
            'button:has-text("Theme")',
            'a:has-text("Dark")',
            'a:has-text("Light")',
            'a:has-text("Theme")'
        ];

        for (const selector of textSelectors) {
            try {
                const element = await page.$(selector);
                if (element) {
                    console.log(`✅ Found dark mode toggle with text selector: ${selector}`);
                    return element;
                }
            } catch (error) {
                // Continue to next selector
            }
        }

        console.log('❌ No dark mode toggle found');
        return null;
    }

    async getCurrentTheme() {
        return await this.page.evaluate(() => {
            const html = document.documentElement;
            const body = document.body;
            
            // Check for dark mode classes
            const isDarkClass = html.classList.contains('dark') || 
                              body.classList.contains('dark') || 
                              html.classList.contains('dark-mode') || 
                              body.classList.contains('dark-mode');
            
            // Check for data attributes
            const isDarkAttr = html.getAttribute('data-theme') === 'dark' || 
                              body.getAttribute('data-theme') === 'dark';
            
            // Check localStorage
            const storedTheme = localStorage.getItem('theme') || localStorage.getItem('darkMode');
            
            return {
                isDarkClass,
                isDarkAttr,
                storedTheme,
                htmlClasses: html.className,
                bodyClasses: body.className,
                computedStyle: window.getComputedStyle(body).backgroundColor
            };
        });
    }

    async findDarkModeToggle() {
        // Try multiple selector strategies
        const selectors = [
            '[data-testid="dark-mode-toggle"]',
            '.dark-mode-toggle',
            '#dark-mode-toggle',
            'button[aria-label*="dark"]',
            'button[title*="dark"]',
            'button[class*="dark"]',
            'button[id*="dark"]',
            '.theme-toggle',
            '#theme-toggle',
            'button[aria-label*="theme"]',
            'button[title*="theme"]'
        ];

        for (const selector of selectors) {
            try {
                const element = await this.page.$(selector);
                if (element) {
                    console.log(`✅ Found dark mode toggle with selector: ${selector}`);
                    return element;
                }
            } catch (error) {
                // Continue to next selector
            }
        }

        // If no toggle found, try to find it by text content
        const textSelectors = [
            'button:has-text("Dark")',
            'button:has-text("Light")',
            'button:has-text("Theme")',
            'a:has-text("Dark")',
            'a:has-text("Light")',
            'a:has-text("Theme")'
        ];

        for (const selector of textSelectors) {
            try {
                const element = await this.page.$(selector);
                if (element) {
                    console.log(`✅ Found dark mode toggle with text selector: ${selector}`);
                    return element;
                }
            } catch (error) {
                // Continue to next selector
            }
        }

        console.log('❌ No dark mode toggle found');
        return null;
    }

    async getCurrentThemeForPage(page) {
        return await page.evaluate(() => {
            const html = document.documentElement;
            const body = document.body;
            
            // Check for dark mode classes
            const isDarkClass = html.classList.contains('dark') || 
                              body.classList.contains('dark') || 
                              html.classList.contains('dark-mode') || 
                              body.classList.contains('dark-mode');
            
            // Check for data attributes
            const isDarkAttr = html.getAttribute('data-theme') === 'dark' || 
                              body.getAttribute('data-theme') === 'dark';
            
            // Check localStorage
            const storedTheme = localStorage.getItem('theme') || localStorage.getItem('darkMode');
            
            return {
                isDarkClass,
                isDarkAttr,
                storedTheme,
                htmlClasses: html.className,
                bodyClasses: body.className,
                computedStyle: window.getComputedStyle(body).backgroundColor
            };
        });
    }

    async analyzeThemeColorsForPage(page) {
        return await page.evaluate(() => {
            const body = document.body;
            const html = document.documentElement;
            
            const bodyStyles = window.getComputedStyle(body);
            const htmlStyles = window.getComputedStyle(html);
            
            // Get various element colors
            const elements = {
                body: bodyStyles.backgroundColor,
                text: bodyStyles.color,
                header: null,
                nav: null,
                footer: null,
                cards: []
            };

            // Check header
            const header = document.querySelector('header, .header');
            if (header) {
                elements.header = window.getComputedStyle(header).backgroundColor;
            }

            // Check nav
            const nav = document.querySelector('nav, .nav, .navbar');
            if (nav) {
                elements.nav = window.getComputedStyle(nav).backgroundColor;
            }

            // Check footer
            const footer = document.querySelector('footer, .footer');
            if (footer) {
                elements.footer = window.getComputedStyle(footer).backgroundColor;
            }

            // Check cards/containers
            const cards = document.querySelectorAll('.card, .container, .content, .section');
            cards.forEach((card, index) => {
                if (index < 5) { // Limit to first 5 cards
                    elements.cards.push({
                        index,
                        background: window.getComputedStyle(card).backgroundColor,
                        color: window.getComputedStyle(card).color
                    });
                }
            });

            return elements;
        });
    }

    async testPage(pageName, url) {
        console.log(`\n🔍 Testing ${pageName} page...`);
        
        let page = null;
        try {
            // Create a new page for each test to avoid session issues
            page = await this.browser.newPage();
            await page.goto(url, { 
                waitUntil: 'networkidle2', 
                timeout: 30000 
            });
            await page.waitForTimeout(1000); // Wait for animations
            
            // Test light mode
            console.log(`📸 Taking ${pageName} light mode screenshot...`);
            const lightTheme = await this.getCurrentThemeForPage(page);
            const lightColors = await this.analyzeThemeColorsForPage(page);
            
            await page.screenshot({
                path: path.join(this.screenshotDir, `${pageName}-light.png`),
                fullPage: true
            });
            
            // Find and click dark mode toggle
            const toggle = await this.findDarkModeToggleForPage(page);
            if (toggle) {
                console.log(`🔄 Clicking dark mode toggle on ${pageName}...`);
                await toggle.click();
                await page.waitForTimeout(1500); // Wait for transition
                
                // Test dark mode
                console.log(`📸 Taking ${pageName} dark mode screenshot...`);
                const darkTheme = await this.getCurrentThemeForPage(page);
                const darkColors = await this.analyzeThemeColorsForPage(page);
                
                await page.screenshot({
                    path: path.join(this.screenshotDir, `${pageName}-dark.png`),
                    fullPage: true
                });
                
                // Store results
                this.testResults[pageName] = {
                    light: { theme: lightTheme, colors: lightColors },
                    dark: { theme: darkTheme, colors: darkColors },
                    toggleFound: true
                };
                
                // Check if colors actually changed
                const colorsChanged = this.compareColors(lightColors, darkColors);
                if (!colorsChanged) {
                    this.testResults.issues.push(`${pageName}: Colors did not change between light and dark mode`);
                }
                
                console.log(`✅ ${pageName} dark mode test completed`);
            } else {
                this.testResults[pageName] = {
                    light: { theme: lightTheme, colors: lightColors },
                    dark: null,
                    toggleFound: false
                };
                this.testResults.issues.push(`${pageName}: Dark mode toggle not found`);
                console.log(`❌ ${pageName}: Dark mode toggle not found`);
            }
            
        } catch (error) {
            console.log(`❌ Error testing ${pageName}:`, error.message);
            this.testResults.issues.push(`${pageName}: ${error.message}`);
        } finally {
            if (page) {
                await page.close();
            }
        }
    }

    compareColors(lightColors, darkColors) {
        // Compare key color properties to see if they changed
        const lightBg = lightColors.body;
        const darkBg = darkColors.body;
        const lightText = lightColors.text;
        const darkText = darkColors.text;
        
        return lightBg !== darkBg || lightText !== darkText;
    }

    async testLocalStoragePersistence() {
        console.log('\n🔍 Testing localStorage persistence...');
        
        try {
            // Go to homepage
            await this.page.goto(this.baseUrl, { waitUntil: 'networkidle2' });
            
            // Check initial state
            const initialState = await this.getCurrentTheme();
            console.log('Initial theme state:', initialState.storedTheme);
            
            // Find and click dark mode toggle
            const toggle = await this.findDarkModeToggle();
            if (toggle) {
                await toggle.click();
                await this.page.waitForTimeout(1000);
                
                // Check localStorage after toggle
                const afterToggle = await this.getCurrentTheme();
                console.log('After toggle:', afterToggle.storedTheme);
                
                // Refresh page and check if preference persists
                await this.page.reload({ waitUntil: 'networkidle2' });
                await this.page.waitForTimeout(1000);
                
                const afterRefresh = await this.getCurrentTheme();
                console.log('After refresh:', afterRefresh.storedTheme);
                
                // Check if dark mode is still active
                const persists = afterRefresh.storedTheme === afterToggle.storedTheme && 
                                (afterRefresh.isDarkClass || afterRefresh.isDarkAttr);
                
                this.testResults.localStorage = {
                    persists,
                    details: {
                        initial: initialState.storedTheme,
                        afterToggle: afterToggle.storedTheme,
                        afterRefresh: afterRefresh.storedTheme,
                        darkModeActive: afterRefresh.isDarkClass || afterRefresh.isDarkAttr
                    }
                };
                
                if (persists) {
                    console.log('✅ Dark mode preference persists across page refresh');
                } else {
                    console.log('❌ Dark mode preference does not persist');
                    this.testResults.issues.push('Dark mode preference does not persist across page refresh');
                }
            } else {
                this.testResults.localStorage = {
                    persists: false,
                    details: 'Dark mode toggle not found'
                };
            }
            
        } catch (error) {
            console.log('❌ Error testing localStorage:', error.message);
            this.testResults.localStorage = {
                persists: false,
                details: error.message
            };
        }
    }

    async generateReport() {
        console.log('\n📊 Generating Dark Mode Test Report...');
        
        const report = {
            timestamp: new Date().toISOString(),
            summary: {
                totalPages: 5,
                pagesWithToggle: 0,
                pagesWithWorkingDarkMode: 0,
                localStoragePersistence: this.testResults.localStorage.persists,
                totalIssues: this.testResults.issues.length
            },
            pageResults: {},
            localStorage: this.testResults.localStorage,
            issues: this.testResults.issues,
            recommendations: []
        };

        // Analyze each page
        const pages = ['homepage', 'about', 'projects', 'blog', 'contact'];
        pages.forEach(page => {
            const result = this.testResults[page];
            if (result) {
                report.pageResults[page] = {
                    toggleFound: result.toggleFound,
                    lightMode: result.light ? 'Working' : 'Not tested',
                    darkMode: result.dark ? 'Working' : 'Not working',
                    colorsChanged: result.light && result.dark ? 
                        this.compareColors(result.light.colors, result.dark.colors) : false
                };
                
                if (result.toggleFound) {
                    report.summary.pagesWithToggle++;
                }
                
                if (result.dark && this.compareColors(result.light.colors, result.dark.colors)) {
                    report.summary.pagesWithWorkingDarkMode++;
                }
            }
        });

        // Generate recommendations
        if (report.summary.pagesWithToggle === 0) {
            report.recommendations.push('Add dark mode toggle buttons to all pages');
        }
        
        if (report.summary.pagesWithWorkingDarkMode < report.summary.pagesWithToggle) {
            report.recommendations.push('Fix dark mode styling on pages where colors are not changing');
        }
        
        if (!report.summary.localStoragePersistence) {
            report.recommendations.push('Implement localStorage persistence for dark mode preference');
        }
        
        if (this.testResults.issues.length > 0) {
            report.recommendations.push('Address JavaScript errors and console warnings');
        }

        // Save report
        const reportPath = path.join(__dirname, '..', 'reports', 'dark-mode-test-report.json');
        const reportsDir = path.dirname(reportPath);
        if (!fs.existsSync(reportsDir)) {
            fs.mkdirSync(reportsDir, { recursive: true });
        }
        
        fs.writeFileSync(reportPath, JSON.stringify(report, null, 2));
        
        console.log('\n' + '='.repeat(60));
        console.log('📋 DARK MODE TEST REPORT');
        console.log('='.repeat(60));
        console.log(`Pages tested: ${report.summary.totalPages}`);
        console.log(`Pages with toggle: ${report.summary.pagesWithToggle}`);
        console.log(`Pages with working dark mode: ${report.summary.pagesWithWorkingDarkMode}`);
        console.log(`localStorage persistence: ${report.summary.localStoragePersistence ? '✅' : '❌'}`);
        console.log(`Total issues: ${report.summary.totalIssues}`);
        
        if (report.issues.length > 0) {
            console.log('\n🔴 Issues Found:');
            report.issues.forEach((issue, index) => {
                console.log(`${index + 1}. ${issue}`);
            });
        }
        
        if (report.recommendations.length > 0) {
            console.log('\n💡 Recommendations:');
            report.recommendations.forEach((rec, index) => {
                console.log(`${index + 1}. ${rec}`);
            });
        }
        
        console.log(`\n📄 Full report saved to: ${reportPath}`);
        console.log(`📸 Screenshots saved to: ${this.screenshotDir}`);
        
        return report;
    }

    async run() {
        try {
            await this.initialize();
            
            // Test all pages
            await this.testPage('homepage', this.baseUrl);
            await this.testPage('about', `${this.baseUrl}/about`);
            await this.testPage('projects', `${this.baseUrl}/projects`);
            await this.testPage('blog', `${this.baseUrl}/blog`);
            await this.testPage('contact', `${this.baseUrl}/contact`);
            
            // Test localStorage persistence
            await this.testLocalStoragePersistence();
            
            // Generate report
            const report = await this.generateReport();
            
            return report;
            
        } catch (error) {
            console.error('❌ Test suite failed:', error);
            throw error;
        } finally {
            if (this.browser) {
                await this.browser.close();
            }
        }
    }
}

// Run the test if this file is executed directly
if (require.main === module) {
    const test = new DarkModeTest();
    test.run().catch(console.error);
}

module.exports = DarkModeTest;