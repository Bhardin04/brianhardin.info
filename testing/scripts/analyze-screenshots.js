const fs = require('fs');
const path = require('path');

function analyzeScreenshots() {
    const screenshotDir = path.join(__dirname, '..', 'screenshots');
    const reportDir = path.join(__dirname, '..', 'reports');
    
    if (!fs.existsSync(screenshotDir)) {
        console.log('❌ Screenshots directory not found');
        return;
    }

    const files = fs.readdirSync(screenshotDir);
    const darkModeFiles = files.filter(file => file.includes('-dark.png'));
    const lightModeFiles = files.filter(file => file.includes('-light.png'));
    
    console.log('📸 Screenshot Analysis Report');
    console.log('='.repeat(50));
    
    console.log('\n✅ Dark Mode Screenshots Found:');
    darkModeFiles.forEach(file => {
        const page = file.replace('-dark.png', '');
        const size = fs.statSync(path.join(screenshotDir, file)).size;
        console.log(`   ${page}: ${file} (${Math.round(size/1024)}KB)`);
    });
    
    console.log('\n✅ Light Mode Screenshots Found:');
    lightModeFiles.forEach(file => {
        const page = file.replace('-light.png', '');
        const size = fs.statSync(path.join(screenshotDir, file)).size;
        console.log(`   ${page}: ${file} (${Math.round(size/1024)}KB)`);
    });
    
    const pages = ['homepage', 'about', 'projects', 'blog', 'contact'];
    
    console.log('\n📊 Page Coverage Analysis:');
    pages.forEach(page => {
        const lightExists = lightModeFiles.some(f => f.includes(page + '-light'));
        const darkExists = darkModeFiles.some(f => f.includes(page + '-dark'));
        
        console.log(`   ${page}:`);
        console.log(`     Light mode: ${lightExists ? '✅' : '❌'}`);
        console.log(`     Dark mode: ${darkExists ? '✅' : '❌'}`);
        console.log(`     Complete: ${lightExists && darkExists ? '✅' : '❌'}`);
    });
    
    console.log('\n📋 Summary:');
    console.log(`   Total screenshots: ${files.length}`);
    console.log(`   Dark mode screenshots: ${darkModeFiles.length}`);
    console.log(`   Light mode screenshots: ${lightModeFiles.length}`);
    console.log(`   Complete page coverage: ${pages.length}/5`);
    
    // Create a summary report
    const summaryReport = {
        timestamp: new Date().toISOString(),
        totalScreenshots: files.length,
        darkModeScreenshots: darkModeFiles.length,
        lightModeScreenshots: lightModeFiles.length,
        pages: pages.map(page => ({
            name: page,
            lightMode: lightModeFiles.some(f => f.includes(page + '-light')),
            darkMode: darkModeFiles.some(f => f.includes(page + '-dark')),
            complete: lightModeFiles.some(f => f.includes(page + '-light')) && 
                     darkModeFiles.some(f => f.includes(page + '-dark'))
        })),
        files: {
            darkMode: darkModeFiles,
            lightMode: lightModeFiles,
            all: files.filter(f => f.endsWith('.png'))
        }
    };
    
    // Save the summary
    const summaryPath = path.join(reportDir, 'screenshot-analysis.json');
    fs.writeFileSync(summaryPath, JSON.stringify(summaryReport, null, 2));
    
    console.log(`\n📄 Analysis saved to: ${summaryPath}`);
    console.log(`📂 Screenshot location: ${screenshotDir}`);
    
    return summaryReport;
}

// Run the analysis
analyzeScreenshots();