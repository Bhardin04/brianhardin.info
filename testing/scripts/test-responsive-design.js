const puppeteer = require('puppeteer');
const fs = require('fs');
const path = require('path');

// Define viewport configurations for testing
const viewports = [
  {
    name: 'Mobile Portrait',
    width: 375,
    height: 667,
    deviceScaleFactor: 2,
    isMobile: true,
    hasTouch: true,
    category: 'mobile'
  },
  {
    name: 'Mobile Landscape',
    width: 667,
    height: 375,
    deviceScaleFactor: 2,
    isMobile: true,
    hasTouch: true,
    category: 'mobile'
  },
  {
    name: 'Tablet Portrait',
    width: 768,
    height: 1024,
    deviceScaleFactor: 2,
    isMobile: true,
    hasTouch: true,
    category: 'tablet'
  },
  {
    name: 'Tablet Landscape',
    width: 1024,
    height: 768,
    deviceScaleFactor: 2,
    isMobile: true,
    hasTouch: true,
    category: 'tablet'
  },
  {
    name: 'Desktop Small',
    width: 1366,
    height: 768,
    deviceScaleFactor: 1,
    isMobile: false,
    hasTouch: false,
    category: 'desktop'
  },
  {
    name: 'Desktop Large',
    width: 1920,
    height: 1080,
    deviceScaleFactor: 1,
    isMobile: false,
    hasTouch: false,
    category: 'desktop'
  }
];

// Pages to test
const pages = [
  { name: 'Homepage', url: 'http://127.0.0.1:8000/' },
  { name: 'Contact', url: 'http://127.0.0.1:8000/contact' },
  { name: 'Resume', url: 'http://127.0.0.1:8000/resume' }
];

// Create screenshots directory
const screenshotDir = path.join(__dirname, 'responsive-screenshots');
if (!fs.existsSync(screenshotDir)) {
  fs.mkdirSync(screenshotDir, { recursive: true });
}

// Test results storage
const testResults = {
  summary: {
    totalTests: 0,
    passedTests: 0,
    failedTests: 0,
    issues: []
  },
  detailed: []
};

// Utility functions
function sanitizeFilename(str) {
  return str.replace(/[^a-z0-9]/gi, '_').toLowerCase();
}

function logIssue(severity, message, page, viewport, screenshot = null) {
  const issue = {
    severity,
    message,
    page: page.name,
    viewport: viewport.name,
    screenshot,
    timestamp: new Date().toISOString()
  };
  testResults.summary.issues.push(issue);
  console.log(`${severity.toUpperCase()}: ${message} (${page.name} - ${viewport.name})`);
}

// Test functions
async function testLayoutIntegrity(page, pageInfo, viewport) {
  const issues = [];

  try {
    // Check for horizontal scrollbar on mobile/tablet
    if (viewport.category !== 'desktop') {
      const bodyWidth = await page.evaluate(() => document.body.scrollWidth);
      const viewportWidth = viewport.width;

      if (bodyWidth > viewportWidth) {
        issues.push({
          type: 'layout',
          severity: 'high',
          message: `Horizontal overflow detected: content width ${bodyWidth}px exceeds viewport width ${viewportWidth}px`
        });
      }
    }

    // Check for elements extending beyond viewport
    const overflowElements = await page.evaluate(() => {
      const elements = document.querySelectorAll('*');
      const overflowing = [];

      elements.forEach(el => {
        const rect = el.getBoundingClientRect();
        if (rect.right > window.innerWidth) {
          overflowing.push({
            tagName: el.tagName,
            className: el.className,
            id: el.id,
            rightPosition: rect.right,
            viewportWidth: window.innerWidth
          });
        }
      });

      return overflowing;
    });

    if (overflowElements.length > 0) {
      issues.push({
        type: 'overflow',
        severity: 'high',
        message: `${overflowElements.length} elements extend beyond viewport`,
        details: overflowElements
      });
    }

  } catch (error) {
    issues.push({
      type: 'error',
      severity: 'medium',
      message: `Error testing layout integrity: ${error.message}`
    });
  }

  return issues;
}

async function testTextReadability(page, pageInfo, viewport) {
  const issues = [];

  try {
    const textIssues = await page.evaluate(() => {
      const problems = [];
      const textElements = document.querySelectorAll('p, h1, h2, h3, h4, h5, h6, span, div, a, button');

      textElements.forEach(el => {
        const computedStyle = window.getComputedStyle(el);
        const fontSize = parseFloat(computedStyle.fontSize);
        const lineHeight = parseFloat(computedStyle.lineHeight);

        // Check minimum font size for readability
        if (fontSize < 14) {
          problems.push({
            type: 'small-text',
            element: el.tagName,
            fontSize: fontSize,
            text: el.textContent.substring(0, 50) + '...'
          });
        }

        // Check line height for readability
        if (lineHeight && lineHeight / fontSize < 1.2) {
          problems.push({
            type: 'tight-line-height',
            element: el.tagName,
            lineHeight: lineHeight,
            fontSize: fontSize,
            ratio: lineHeight / fontSize
          });
        }
      });

      return problems;
    });

    if (textIssues.length > 0) {
      issues.push({
        type: 'readability',
        severity: 'medium',
        message: `${textIssues.length} text readability issues found`,
        details: textIssues
      });
    }

  } catch (error) {
    issues.push({
      type: 'error',
      severity: 'low',
      message: `Error testing text readability: ${error.message}`
    });
  }

  return issues;
}

async function testTapTargets(page, pageInfo, viewport) {
  const issues = [];

  if (viewport.hasTouch) {
    try {
      const tapTargetIssues = await page.evaluate(() => {
        const problems = [];
        const interactiveElements = document.querySelectorAll('a, button, input, select, textarea, [onclick], [role="button"]');

        interactiveElements.forEach(el => {
          const rect = el.getBoundingClientRect();
          const width = rect.width;
          const height = rect.height;

          // Minimum tap target size should be 44x44px
          if (width < 44 || height < 44) {
            problems.push({
              type: 'small-tap-target',
              element: el.tagName,
              width: width,
              height: height,
              text: el.textContent || el.value || el.alt || 'No text'
            });
          }
        });

        return problems;
      });

      if (tapTargetIssues.length > 0) {
        issues.push({
          type: 'tap-targets',
          severity: 'high',
          message: `${tapTargetIssues.length} tap targets smaller than 44x44px`,
          details: tapTargetIssues
        });
      }

    } catch (error) {
      issues.push({
        type: 'error',
        severity: 'low',
        message: `Error testing tap targets: ${error.message}`
      });
    }
  }

  return issues;
}

async function testNavigation(page, pageInfo, viewport) {
  const issues = [];

  try {
    const navIssues = await page.evaluate(() => {
      const problems = [];
      const navElements = document.querySelectorAll('nav, [role="navigation"], .navbar, .nav-menu');

      navElements.forEach(nav => {
        const rect = nav.getBoundingClientRect();

        // Check if navigation is visible
        if (rect.width === 0 || rect.height === 0) {
          problems.push({
            type: 'hidden-navigation',
            element: nav.tagName,
            className: nav.className
          });
        }

        // Check for navigation links
        const links = nav.querySelectorAll('a');
        if (links.length === 0) {
          problems.push({
            type: 'no-nav-links',
            element: nav.tagName,
            className: nav.className
          });
        }
      });

      return problems;
    });

    if (navIssues.length > 0) {
      issues.push({
        type: 'navigation',
        severity: 'medium',
        message: `${navIssues.length} navigation issues found`,
        details: navIssues
      });
    }

  } catch (error) {
    issues.push({
      type: 'error',
      severity: 'low',
      message: `Error testing navigation: ${error.message}`
    });
  }

  return issues;
}

async function testImages(page, pageInfo, viewport) {
  const issues = [];

  try {
    const imageIssues = await page.evaluate(() => {
      const problems = [];
      const images = document.querySelectorAll('img');

      images.forEach(img => {
        const rect = img.getBoundingClientRect();

        // Check if image extends beyond viewport
        if (rect.right > window.innerWidth) {
          problems.push({
            type: 'image-overflow',
            src: img.src,
            width: rect.width,
            viewportWidth: window.innerWidth
          });
        }

        // Check for missing alt text
        if (!img.alt) {
          problems.push({
            type: 'missing-alt',
            src: img.src
          });
        }
      });

      return problems;
    });

    if (imageIssues.length > 0) {
      issues.push({
        type: 'images',
        severity: 'medium',
        message: `${imageIssues.length} image issues found`,
        details: imageIssues
      });
    }

  } catch (error) {
    issues.push({
      type: 'error',
      severity: 'low',
      message: `Error testing images: ${error.message}`
    });
  }

  return issues;
}

async function testForms(page, pageInfo, viewport) {
  const issues = [];

  try {
    const formIssues = await page.evaluate(() => {
      const problems = [];
      const forms = document.querySelectorAll('form');

      forms.forEach(form => {
        const inputs = form.querySelectorAll('input, textarea, select');

        inputs.forEach(input => {
          const rect = input.getBoundingClientRect();

          // Check minimum size for form elements
          if (rect.height < 44) {
            problems.push({
              type: 'small-form-element',
              element: input.tagName,
              type: input.type,
              height: rect.height,
              name: input.name || input.id
            });
          }
        });
      });

      return problems;
    });

    if (formIssues.length > 0) {
      issues.push({
        type: 'forms',
        severity: 'medium',
        message: `${formIssues.length} form usability issues found`,
        details: formIssues
      });
    }

  } catch (error) {
    issues.push({
      type: 'error',
      severity: 'low',
      message: `Error testing forms: ${error.message}`
    });
  }

  return issues;
}

async function runResponsiveTests() {
  console.log('Starting responsive design tests...');
  console.log('Testing website: brianhardin.info');
  console.log('Total test combinations:', viewports.length * pages.length);
  console.log('');

  const browser = await puppeteer.launch({
    headless: true,
    defaultViewport: null,
    args: ['--no-sandbox', '--disable-setuid-sandbox']
  });

  try {
    for (const pageInfo of pages) {
      for (const viewport of viewports) {
        testResults.summary.totalTests++;

        console.log(`Testing ${pageInfo.name} on ${viewport.name} (${viewport.width}x${viewport.height})`);

        const page = await browser.newPage();
        await page.setViewport(viewport);

        const testResult = {
          page: pageInfo.name,
          viewport: viewport.name,
          url: pageInfo.url,
          dimensions: `${viewport.width}x${viewport.height}`,
          category: viewport.category,
          issues: [],
          screenshot: null,
          timestamp: new Date().toISOString()
        };

        try {
          // Navigate to page
          await page.goto(pageInfo.url, { waitUntil: 'networkidle2', timeout: 30000 });

          // Wait for page to fully load
          await page.waitForTimeout(2000);

          // Run all tests
          const layoutIssues = await testLayoutIntegrity(page, pageInfo, viewport);
          const textIssues = await testTextReadability(page, pageInfo, viewport);
          const tapTargetIssues = await testTapTargets(page, pageInfo, viewport);
          const navIssues = await testNavigation(page, pageInfo, viewport);
          const imageIssues = await testImages(page, pageInfo, viewport);
          const formIssues = await testForms(page, pageInfo, viewport);

          const allIssues = [
            ...layoutIssues,
            ...textIssues,
            ...tapTargetIssues,
            ...navIssues,
            ...imageIssues,
            ...formIssues
          ];

          testResult.issues = allIssues;

          // Take screenshot
          const screenshotPath = path.join(screenshotDir, `${sanitizeFilename(pageInfo.name)}_${sanitizeFilename(viewport.name)}.png`);
          await page.screenshot({ path: screenshotPath, fullPage: true });
          testResult.screenshot = screenshotPath;

          // Log issues
          allIssues.forEach(issue => {
            logIssue(issue.severity, issue.message, pageInfo, viewport, screenshotPath);
          });

          if (allIssues.length === 0) {
            testResults.summary.passedTests++;
            console.log(`✓ PASS: No issues found`);
          } else {
            testResults.summary.failedTests++;
            console.log(`✗ FAIL: ${allIssues.length} issues found`);
          }

        } catch (error) {
          testResult.issues.push({
            type: 'error',
            severity: 'high',
            message: `Failed to test page: ${error.message}`
          });

          logIssue('high', `Failed to test page: ${error.message}`, pageInfo, viewport);
          testResults.summary.failedTests++;
        }

        testResults.detailed.push(testResult);
        await page.close();
        console.log('');
      }
    }

  } finally {
    await browser.close();
  }

  // Generate report
  await generateReport();
}

async function generateReport() {
  const reportContent = `# Responsive Design Test Report
Generated: ${new Date().toISOString()}
Website: brianhardin.info (http://127.0.0.1:8000)

## Summary
- Total Tests: ${testResults.summary.totalTests}
- Passed: ${testResults.summary.passedTests}
- Failed: ${testResults.summary.failedTests}
- Success Rate: ${((testResults.summary.passedTests / testResults.summary.totalTests) * 100).toFixed(1)}%

## Issues by Severity
${generateIssuesSummary()}

## Detailed Results by Viewport and Page
${generateDetailedResults()}

## Recommendations
${generateRecommendations()}

## Screenshots
All screenshots have been saved to: ${screenshotDir}
`;

  const reportPath = path.join(__dirname, 'responsive-design-report.md');
  fs.writeFileSync(reportPath, reportContent);

  console.log('='.repeat(60));
  console.log('RESPONSIVE DESIGN TEST SUMMARY');
  console.log('='.repeat(60));
  console.log(`Total Tests: ${testResults.summary.totalTests}`);
  console.log(`Passed: ${testResults.summary.passedTests}`);
  console.log(`Failed: ${testResults.summary.failedTests}`);
  console.log(`Success Rate: ${((testResults.summary.passedTests / testResults.summary.totalTests) * 100).toFixed(1)}%`);
  console.log('');
  console.log(`Report saved to: ${reportPath}`);
  console.log(`Screenshots saved to: ${screenshotDir}`);
  console.log('');

  if (testResults.summary.issues.length > 0) {
    console.log('KEY ISSUES FOUND:');
    testResults.summary.issues.forEach((issue, index) => {
      console.log(`${index + 1}. [${issue.severity.toUpperCase()}] ${issue.message}`);
      console.log(`   Page: ${issue.page}, Viewport: ${issue.viewport}`);
    });
  } else {
    console.log('✓ No responsive design issues found!');
  }
}

function generateIssuesSummary() {
  const severityCounts = {
    high: 0,
    medium: 0,
    low: 0
  };

  testResults.summary.issues.forEach(issue => {
    severityCounts[issue.severity]++;
  });

  return `- High Priority: ${severityCounts.high}
- Medium Priority: ${severityCounts.medium}
- Low Priority: ${severityCounts.low}
- Total Issues: ${testResults.summary.issues.length}`;
}

function generateDetailedResults() {
  return testResults.detailed.map(result => {
    const issueCount = result.issues.length;
    const status = issueCount === 0 ? '✓ PASS' : `✗ FAIL (${issueCount} issues)`;

    let details = `### ${result.page} - ${result.viewport} (${result.dimensions})
**Status:** ${status}
**Category:** ${result.category}
`;

    if (result.issues.length > 0) {
      details += `**Issues:**\n`;
      result.issues.forEach((issue, index) => {
        details += `${index + 1}. [${issue.severity.toUpperCase()}] ${issue.message}\n`;
      });
    }

    details += `**Screenshot:** ${result.screenshot}\n`;

    return details;
  }).join('\n');
}

function generateRecommendations() {
  const recommendations = [];

  // Analyze common issues and provide recommendations
  const issueTypes = {};
  testResults.summary.issues.forEach(issue => {
    const type = issue.message.split(':')[0] || 'general';
    issueTypes[type] = (issueTypes[type] || 0) + 1;
  });

  if (issueTypes['Horizontal overflow detected']) {
    recommendations.push('- **Fix horizontal overflow**: Ensure all content fits within viewport widths, especially on mobile devices. Use max-width: 100% and overflow-x: hidden where appropriate.');
  }

  if (issueTypes['tap targets smaller than 44x44px']) {
    recommendations.push('- **Improve tap targets**: Increase the size of buttons and links to at least 44x44px for better mobile usability.');
  }

  if (issueTypes['text readability issues']) {
    recommendations.push('- **Enhance text readability**: Ensure minimum font sizes (14px+) and adequate line heights (1.4+) for better readability across devices.');
  }

  if (issueTypes['image issues']) {
    recommendations.push('- **Optimize images**: Ensure images are responsive and include alt text for accessibility.');
  }

  if (recommendations.length === 0) {
    recommendations.push('- **Great job!** No major responsive design issues were found. The website appears to be well-optimized for different screen sizes.');
  }

  return recommendations.join('\n');
}

// Run the tests
runResponsiveTests().catch(console.error);
