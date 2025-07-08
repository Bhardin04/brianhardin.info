const puppeteer = require('puppeteer');
const fs = require('fs');

(async () => {
  let browser;
  try {
    browser = await puppeteer.launch({
      headless: false,
      defaultViewport: {
        width: 1920,
        height: 1080
      },
      args: ['--no-sandbox', '--disable-setuid-sandbox']
    });
    
    const page = await browser.newPage();
    
    // Handle page errors
    page.on('error', (err) => {
      console.error('Page error:', err);
    });
    
    page.on('pageerror', (err) => {
      console.error('Page error:', err);
    });
  
  try {
    console.log('Navigating to homepage...');
    await page.goto('http://127.0.0.1:8000', { waitUntil: 'networkidle2' });
    
    // Wait for page to fully load
    await page.waitForTimeout(2000);
    
    console.log('Taking light mode screenshot...');
    await page.screenshot({ 
      path: 'homepage-light-after-fix.png',
      fullPage: true 
    });
    
    // Look for dark mode toggle button
    console.log('Looking for dark mode toggle button...');
    
    // Try multiple possible selectors for the dark mode toggle
    const possibleSelectors = [
      '[data-theme-toggle]',
      '.theme-toggle',
      '#theme-toggle',
      '.dark-mode-toggle',
      'button[aria-label*="dark"]',
      'button[aria-label*="theme"]',
      '.nav-link[href*="theme"]',
      'button:has-text("Dark")',
      'button:has-text("Light")',
      '.toggle-switch',
      '.theme-switcher'
    ];
    
    let toggleButton = null;
    let usedSelector = null;
    
    for (const selector of possibleSelectors) {
      try {
        const element = await page.$(selector);
        if (element) {
          toggleButton = element;
          usedSelector = selector;
          console.log(`Found toggle button with selector: ${selector}`);
          break;
        }
      } catch (e) {
        // Continue to next selector
      }
    }
    
    // If no specific toggle found, look for any button in the navigation
    if (!toggleButton) {
      console.log('Looking for any buttons in navigation...');
      const navButtons = await page.$$('nav button, .navbar button, header button');
      if (navButtons.length > 0) {
        toggleButton = navButtons[0];
        usedSelector = 'nav button (first found)';
        console.log(`Using first navigation button as toggle`);
      }
    }
    
    // If still no toggle found, check for any clickable elements that might be the toggle
    if (!toggleButton) {
      console.log('Looking for any clickable elements that might be theme toggle...');
      const clickableElements = await page.$$('a, button, [onclick], [data-toggle]');
      
      for (const element of clickableElements) {
        const text = await page.evaluate(el => el.textContent?.toLowerCase() || '', element);
        const ariaLabel = await page.evaluate(el => el.getAttribute('aria-label')?.toLowerCase() || '', element);
        const className = await page.evaluate(el => el.className?.toLowerCase() || '', element);
        
        if (text.includes('dark') || text.includes('theme') || text.includes('mode') ||
            ariaLabel.includes('dark') || ariaLabel.includes('theme') || ariaLabel.includes('mode') ||
            className.includes('dark') || className.includes('theme') || className.includes('toggle')) {
          toggleButton = element;
          usedSelector = 'detected by content analysis';
          console.log(`Found potential toggle with text: "${text}", aria-label: "${ariaLabel}", class: "${className}"`);
          break;
        }
      }
    }
    
    if (toggleButton) {
      console.log(`Clicking dark mode toggle (${usedSelector})...`);
      await toggleButton.click();
      
      // Wait for theme transition
      await page.waitForTimeout(1000);
      
      console.log('Taking dark mode screenshot...');
      await page.screenshot({ 
        path: 'homepage-dark-after-fix.png',
        fullPage: true 
      });
      
      console.log('Screenshots captured successfully!');
      
      // Analyze the page elements for dark mode changes
      console.log('Analyzing page elements...');
      
      const analysis = await page.evaluate(() => {
        const results = {
          bodyBackground: getComputedStyle(document.body).backgroundColor,
          bodyColor: getComputedStyle(document.body).color,
          navElements: [],
          headingElements: [],
          linkElements: [],
          buttonElements: [],
          toggleButtonInfo: null
        };
        
        // Analyze navigation elements
        const navElements = document.querySelectorAll('nav, .navbar, header');
        navElements.forEach((nav, index) => {
          const styles = getComputedStyle(nav);
          results.navElements.push({
            index,
            backgroundColor: styles.backgroundColor,
            color: styles.color,
            tagName: nav.tagName
          });
        });
        
        // Analyze headings
        const headings = document.querySelectorAll('h1, h2, h3, h4, h5, h6');
        headings.forEach((heading, index) => {
          const styles = getComputedStyle(heading);
          results.headingElements.push({
            index,
            text: heading.textContent?.substring(0, 50) || '',
            color: styles.color,
            tagName: heading.tagName
          });
        });
        
        // Analyze links
        const links = document.querySelectorAll('a');
        links.forEach((link, index) => {
          const styles = getComputedStyle(link);
          results.linkElements.push({
            index,
            text: link.textContent?.substring(0, 30) || '',
            color: styles.color,
            href: link.href
          });
        });
        
        // Analyze buttons
        const buttons = document.querySelectorAll('button');
        buttons.forEach((button, index) => {
          const styles = getComputedStyle(button);
          results.buttonElements.push({
            index,
            text: button.textContent?.substring(0, 30) || '',
            backgroundColor: styles.backgroundColor,
            color: styles.color,
            border: styles.border
          });
        });
        
        // Try to find and analyze the toggle button specifically
        const possibleToggles = document.querySelectorAll('button, [data-theme-toggle], .theme-toggle, .dark-mode-toggle');
        possibleToggles.forEach(toggle => {
          const text = toggle.textContent?.toLowerCase() || '';
          const ariaLabel = toggle.getAttribute('aria-label')?.toLowerCase() || '';
          const className = toggle.className?.toLowerCase() || '';
          
          if (text.includes('dark') || text.includes('theme') || text.includes('mode') ||
              ariaLabel.includes('dark') || ariaLabel.includes('theme') || ariaLabel.includes('mode') ||
              className.includes('dark') || className.includes('theme') || className.includes('toggle')) {
            const styles = getComputedStyle(toggle);
            results.toggleButtonInfo = {
              text: toggle.textContent,
              backgroundColor: styles.backgroundColor,
              color: styles.color,
              border: styles.border,
              visibility: styles.visibility,
              opacity: styles.opacity,
              className: toggle.className,
              ariaLabel: toggle.getAttribute('aria-label')
            };
          }
        });
        
        return results;
      });
      
      // Save analysis to file
      fs.writeFileSync('dark-mode-analysis.json', JSON.stringify(analysis, null, 2));
      console.log('Analysis saved to dark-mode-analysis.json');
      
    } else {
      console.log('Could not find dark mode toggle button. Taking screenshots anyway...');
      
      // Take a second screenshot anyway in case there's an automatic theme
      await page.waitForTimeout(3000);
      await page.screenshot({ 
        path: 'homepage-dark-after-fix.png',
        fullPage: true 
      });
    }
    
  } catch (error) {
    console.error('Error during test:', error);
  } finally {
    if (page) {
      await page.close();
    }
  }
  
  } catch (error) {
    console.error('Error launching browser:', error);
  } finally {
    if (browser) {
      await browser.close();
    }
  }
})().catch(console.error);