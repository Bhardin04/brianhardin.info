const puppeteer = require('puppeteer');
const fs = require('fs');
const path = require('path');

class ComprehensiveDarkModeTest {
    constructor() {
        this.baseUrl = 'http://127.0.0.1:8000';
        this.screenshotDir = path.join(__dirname, '..', 'screenshots');
        this.reportDir = path.join(__dirname, '..', 'reports');
        this.browser = null;
        this.results = {
            timestamp: new Date().toISOString(),
            pages: {},
            summary: {
                totalPages: 0,
                pagesWithToggle: 0,
                pagesWithWorkingDarkMode: 0,
                localStoragePersistence: false,
                issues: []
            }
        };
    }

    async initialize() {
        console.log('🚀 Initializing Comprehensive Dark Mode Test...');

        // Create directories
        [this.screenshotDir, this.reportDir].forEach(dir => {
            if (!fs.existsSync(dir)) {
                fs.mkdirSync(dir, { recursive: true });
            }
        });

        this.browser = await puppeteer.launch({
            headless: true,
            defaultViewport: { width: 1366, height: 768 },
            args: ['--no-sandbox', '--disable-setuid-sandbox']
        });
    }

    async resetTheme() {
        // Reset to light mode by clearing localStorage
        const page = await this.browser.newPage();
        await page.goto(this.baseUrl);
        await page.evaluate(() => {
            localStorage.removeItem('theme');
            document.documentElement.classList.remove('dark');
        });
        await page.close();
    }

    async testPage(pageName, pagePath) {
        console.log(`\n🔍 Testing ${pageName} page...`);

        const page = await this.browser.newPage();
        const pageResult = {
            name: pageName,
            path: pagePath,
            hasToggle: false,
            lightMode: null,
            darkMode: null,
            toggleWorks: false,
            themeColors: {
                light: null,
                dark: null
            },
            errors: []
        };

        try {
            // Navigate to page
            await page.goto(`${this.baseUrl}${pagePath}`, { waitUntil: 'networkidle2' });
            await page.waitForTimeout(1000);

            // Check for toggle
            const toggle = await page.$('#theme-toggle');
            pageResult.hasToggle = toggle !== null;

            // Get light mode state
            const lightState = await page.evaluate(() => {
                const html = document.documentElement;
                const body = document.body;
                return {
                    isDark: html.classList.contains('dark'),
                    storedTheme: localStorage.getItem('theme'),
                    htmlClasses: html.className,
                    bodyBackground: window.getComputedStyle(body).backgroundColor,
                    bodyColor: window.getComputedStyle(body).color
                };
            });

            pageResult.lightMode = lightState;

            // Take light mode screenshot
            console.log(`📸 Taking ${pageName} light mode screenshot...`);
            await page.screenshot({
                path: path.join(this.screenshotDir, `${pageName}-light.png`),
                fullPage: true
            });

            // Analyze colors in light mode
            const lightColors = await this.analyzeColors(page);
            pageResult.themeColors.light = lightColors;

            // Test dark mode toggle
            if (pageResult.hasToggle) {
                console.log(`🔄 Testing dark mode toggle on ${pageName}...`);

                // Method 1: Try clicking the toggle
                try {
                    await toggle.click();
                    await page.waitForTimeout(1000);
                    pageResult.toggleWorks = true;
                    console.log(`✅ Toggle clicked successfully on ${pageName}`);
                } catch (error) {
                    console.log(`⚠️ Toggle click failed, using JavaScript on ${pageName}`);
                    // Method 2: Use JavaScript to simulate toggle
                    await page.evaluate(() => {
                        document.documentElement.classList.add('dark');
                        localStorage.setItem('theme', 'dark');
                    });
                    await page.waitForTimeout(500);
                    pageResult.errors.push(`Toggle click failed: ${error.message}`);
                }

                // Get dark mode state
                const darkState = await page.evaluate(() => {
                    const html = document.documentElement;
                    const body = document.body;
                    return {
                        isDark: html.classList.contains('dark'),
                        storedTheme: localStorage.getItem('theme'),
                        htmlClasses: html.className,
                        bodyBackground: window.getComputedStyle(body).backgroundColor,
                        bodyColor: window.getComputedStyle(body).color
                    };
                });

                pageResult.darkMode = darkState;

                // Take dark mode screenshot
                console.log(`📸 Taking ${pageName} dark mode screenshot...`);
                await page.screenshot({
                    path: path.join(this.screenshotDir, `${pageName}-dark.png`),
                    fullPage: true
                });

                // Analyze colors in dark mode
                const darkColors = await this.analyzeColors(page);
                pageResult.themeColors.dark = darkColors;

                console.log(`✅ ${pageName} test completed`);
            } else {
                pageResult.errors.push('Dark mode toggle not found');
                console.log(`❌ ${pageName}: Dark mode toggle not found`);
            }

        } catch (error) {
            pageResult.errors.push(error.message);
            console.log(`❌ Error testing ${pageName}:`, error.message);
        } finally {
            await page.close();
        }

        this.results.pages[pageName] = pageResult;
        return pageResult;
    }

    async analyzeColors(page) {
        return await page.evaluate(() => {
            const body = document.body;
            const nav = document.querySelector('nav');
            const footer = document.querySelector('footer');
            const main = document.querySelector('main');

            const getStyle = (element) => {
                if (!element) return null;
                const style = window.getComputedStyle(element);
                return {
                    background: style.backgroundColor,
                    color: style.color,
                    border: style.borderColor
                };
            };

            return {
                body: getStyle(body),
                nav: getStyle(nav),
                footer: getStyle(footer),
                main: getStyle(main)
            };
        });
    }

    async testLocalStoragePersistence() {
        console.log('\n🔍 Testing localStorage persistence...');

        const page = await this.browser.newPage();
        try {
            // Go to homepage
            await page.goto(this.baseUrl);
            await page.waitForTimeout(1000);

            // Set dark mode
            await page.evaluate(() => {
                document.documentElement.classList.add('dark');
                localStorage.setItem('theme', 'dark');
            });

            // Check if it's set
            const afterSet = await page.evaluate(() => ({
                isDark: document.documentElement.classList.contains('dark'),
                stored: localStorage.getItem('theme')
            }));

            // Refresh page
            await page.reload({ waitUntil: 'networkidle2' });
            await page.waitForTimeout(1000);

            // Check if it persisted
            const afterReload = await page.evaluate(() => ({
                isDark: document.documentElement.classList.contains('dark'),
                stored: localStorage.getItem('theme')
            }));

            const persists = afterReload.isDark && afterReload.stored === 'dark';
            this.results.summary.localStoragePersistence = persists;

            console.log(`📊 localStorage persistence: ${persists ? '✅' : '❌'}`);
            console.log(`   After set: isDark=${afterSet.isDark}, stored=${afterSet.stored}`);
            console.log(`   After reload: isDark=${afterReload.isDark}, stored=${afterReload.stored}`);

        } catch (error) {
            this.results.summary.issues.push(`localStorage test failed: ${error.message}`);
            console.log(`❌ localStorage test failed:`, error.message);
        } finally {
            await page.close();
        }
    }

    async generateReport() {
        console.log('\n📊 Generating comprehensive report...');

        // Calculate summary statistics
        const pages = Object.values(this.results.pages);
        this.results.summary.totalPages = pages.length;
        this.results.summary.pagesWithToggle = pages.filter(p => p.hasToggle).length;
        this.results.summary.pagesWithWorkingDarkMode = pages.filter(p =>
            p.hasToggle && p.darkMode && p.darkMode.isDark
        ).length;

        // Collect all issues
        pages.forEach(page => {
            page.errors.forEach(error => {
                this.results.summary.issues.push(`${page.name}: ${error}`);
            });
        });

        // Analyze component behavior
        const componentAnalysis = this.analyzeComponentBehavior();
        this.results.componentAnalysis = componentAnalysis;

        // Generate recommendations
        const recommendations = this.generateRecommendations();
        this.results.recommendations = recommendations;

        // Save full report
        const reportPath = path.join(this.reportDir, 'comprehensive-dark-mode-report.json');
        fs.writeFileSync(reportPath, JSON.stringify(this.results, null, 2));

        // Generate human-readable report
        this.printReport();

        console.log(`\n📄 Full report saved to: ${reportPath}`);
        console.log(`📸 Screenshots saved to: ${this.screenshotDir}`);

        return this.results;
    }

    analyzeComponentBehavior() {
        const analysis = {
            consistentComponents: [],
            problematicComponents: [],
            colorChangeAnalysis: {}
        };

        const pages = Object.values(this.results.pages);

        pages.forEach(page => {
            if (page.lightMode && page.darkMode && page.themeColors.light && page.themeColors.dark) {
                const light = page.themeColors.light;
                const dark = page.themeColors.dark;

                // Check if colors actually changed
                const bodyChanged = light.body?.background !== dark.body?.background;
                const navChanged = light.nav?.background !== dark.nav?.background;
                const footerChanged = light.footer?.background !== dark.footer?.background;

                analysis.colorChangeAnalysis[page.name] = {
                    bodyChanged,
                    navChanged,
                    footerChanged,
                    overallWorking: bodyChanged && navChanged && footerChanged
                };

                if (bodyChanged && navChanged && footerChanged) {
                    analysis.consistentComponents.push(page.name);
                } else {
                    analysis.problematicComponents.push(page.name);
                }
            }
        });

        return analysis;
    }

    generateRecommendations() {
        const recommendations = [];
        const summary = this.results.summary;
        const componentAnalysis = this.results.componentAnalysis;

        if (summary.pagesWithToggle < summary.totalPages) {
            recommendations.push('Add dark mode toggle to all pages');
        }

        if (summary.pagesWithWorkingDarkMode < summary.pagesWithToggle) {
            recommendations.push('Fix dark mode implementation on pages where it\'s not working');
        }

        if (!summary.localStoragePersistence) {
            recommendations.push('Fix localStorage persistence for dark mode preference');
        }

        if (componentAnalysis.problematicComponents.length > 0) {
            recommendations.push(`Fix component styling on: ${componentAnalysis.problematicComponents.join(', ')}`);
        }

        if (summary.issues.length > 0) {
            recommendations.push('Address JavaScript errors and implementation issues');
        }

        return recommendations;
    }

    printReport() {
        console.log('\n' + '='.repeat(70));
        console.log('📋 COMPREHENSIVE DARK MODE TEST REPORT');
        console.log('='.repeat(70));

        const summary = this.results.summary;
        console.log(`📊 Summary:`);
        console.log(`   Total pages tested: ${summary.totalPages}`);
        console.log(`   Pages with toggle: ${summary.pagesWithToggle}`);
        console.log(`   Pages with working dark mode: ${summary.pagesWithWorkingDarkMode}`);
        console.log(`   localStorage persistence: ${summary.localStoragePersistence ? '✅' : '❌'}`);
        console.log(`   Total issues found: ${summary.issues.length}`);

        console.log('\n📄 Page Details:');
        Object.values(this.results.pages).forEach(page => {
            console.log(`\n   ${page.name.toUpperCase()}:`);
            console.log(`     Toggle found: ${page.hasToggle ? '✅' : '❌'}`);
            console.log(`     Toggle works: ${page.toggleWorks ? '✅' : '❌'}`);
            console.log(`     Dark mode active: ${page.darkMode?.isDark ? '✅' : '❌'}`);
            console.log(`     Light bg: ${page.lightMode?.bodyBackground || 'Unknown'}`);
            console.log(`     Dark bg: ${page.darkMode?.bodyBackground || 'Unknown'}`);

            if (page.errors.length > 0) {
                console.log(`     Errors: ${page.errors.join(', ')}`);
            }
        });

        if (this.results.componentAnalysis) {
            console.log('\n🎨 Component Analysis:');
            const analysis = this.results.componentAnalysis;
            console.log(`   Consistent components: ${analysis.consistentComponents.join(', ') || 'None'}`);
            console.log(`   Problematic components: ${analysis.problematicComponents.join(', ') || 'None'}`);
        }

        if (summary.issues.length > 0) {
            console.log('\n🔴 Issues Found:');
            summary.issues.forEach((issue, index) => {
                console.log(`   ${index + 1}. ${issue}`);
            });
        }

        if (this.results.recommendations && this.results.recommendations.length > 0) {
            console.log('\n💡 Recommendations:');
            this.results.recommendations.forEach((rec, index) => {
                console.log(`   ${index + 1}. ${rec}`);
            });
        }
    }

    async run() {
        try {
            await this.initialize();

            // Reset to light mode first
            await this.resetTheme();

            // Test all pages
            const pages = [
                { name: 'homepage', path: '/' },
                { name: 'about', path: '/about' },
                { name: 'projects', path: '/projects' },
                { name: 'blog', path: '/blog' },
                { name: 'contact', path: '/contact' }
            ];

            for (const page of pages) {
                await this.testPage(page.name, page.path);
                // Small delay between tests
                await new Promise(resolve => setTimeout(resolve, 500));
            }

            // Test localStorage persistence
            await this.testLocalStoragePersistence();

            // Generate final report
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

// Run the test if executed directly
if (require.main === module) {
    const test = new ComprehensiveDarkModeTest();
    test.run().catch(console.error);
}

module.exports = ComprehensiveDarkModeTest;
