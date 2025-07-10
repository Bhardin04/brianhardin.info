/**
 * Error Boundary System
 * Provides component-level error boundaries with graceful fallbacks
 */

class ErrorBoundary {
    constructor(element, options = {}) {
        this.element = element;
        this.originalContent = element.innerHTML;
        this.options = {
            fallbackComponent: options.fallbackComponent || this.getDefaultFallback(),
            onError: options.onError || this.defaultErrorHandler,
            retryable: options.retryable !== false,
            isolate: options.isolate !== false,
            logErrors: options.logErrors !== false,
            ...options
        };
        this.errorCount = 0;
        this.lastError = null;
        this.isInErrorState = false;
        this.retryAttempts = 0;
        this.maxRetries = options.maxRetries || 3;
        
        this.initialize();
    }

    /**
     * Initialize error boundary
     */
    initialize() {
        this.setupErrorCatching();
        this.addBoundaryMarker();
    }

    /**
     * Setup error catching for the element
     */
    setupErrorCatching() {
        // Catch JavaScript errors within this boundary
        if (this.options.isolate) {
            this.wrapScripts();
        }

        // Catch async errors
        this.setupAsyncErrorCatching();

        // Catch resource loading errors
        this.setupResourceErrorCatching();

        // Catch render errors
        this.setupRenderErrorCatching();
    }

    /**
     * Wrap scripts within the boundary
     */
    wrapScripts() {
        const scripts = this.element.querySelectorAll('script');
        scripts.forEach(script => {
            if (script.src) {
                // External script
                script.addEventListener('error', (e) => {
                    this.handleError({
                        type: 'script_load_error',
                        message: `Failed to load script: ${script.src}`,
                        source: script.src,
                        element: script
                    });
                });
            } else {
                // Inline script - wrap in try-catch
                const originalCode = script.textContent;
                script.textContent = `
                    try {
                        ${originalCode}
                    } catch (error) {
                        if (window.ErrorBoundary) {
                            const boundary = ErrorBoundary.findBoundaryForElement(this);
                            if (boundary) {
                                boundary.handleError({
                                    type: 'inline_script_error',
                                    message: error.message,
                                    error: error,
                                    element: this
                                });
                            }
                        }
                    }
                `;
            }
        });
    }

    /**
     * Setup async error catching
     */
    setupAsyncErrorCatching() {
        // Wrap fetch calls within this boundary
        this.wrapAsyncFunctions();
        
        // Monitor promise rejections
        this.monitorPromiseRejections();
    }

    /**
     * Wrap async functions
     */
    wrapAsyncFunctions() {
        // This is a simplified implementation
        // In practice, you'd need more sophisticated wrapping
        const originalFetch = window.fetch;
        
        // Store reference to this boundary
        const boundary = this;
        
        // Override fetch for elements within this boundary
        if (this.element.id) {
            const boundaryId = this.element.id;
            
            // Add data attribute to track boundary context
            this.element.setAttribute('data-error-boundary', boundaryId);
            
            // Elements within this boundary can reference it
            this.element.addEventListener('fetch-error', (e) => {
                boundary.handleError({
                    type: 'fetch_error',
                    message: e.detail.message,
                    error: e.detail.error,
                    url: e.detail.url
                });
            });
        }
    }

    /**
     * Monitor promise rejections within boundary
     */
    monitorPromiseRejections() {
        // Track unhandled promise rejections that might belong to this boundary
        const boundary = this;
        
        window.addEventListener('unhandledrejection', (e) => {
            // Try to determine if this rejection belongs to our boundary
            if (boundary.isPromiseFromBoundary(e.promise)) {
                boundary.handleError({
                    type: 'promise_rejection',
                    message: e.reason?.message || 'Unhandled promise rejection',
                    error: e.reason,
                    promise: e.promise
                });
                
                // Prevent global error handler
                e.preventDefault();
            }
        });
    }

    /**
     * Setup resource error catching
     */
    setupResourceErrorCatching() {
        const resources = this.element.querySelectorAll('img, link, script, iframe');
        
        resources.forEach(resource => {
            resource.addEventListener('error', (e) => {
                this.handleError({
                    type: 'resource_error',
                    message: `Failed to load ${resource.tagName.toLowerCase()}: ${resource.src || resource.href}`,
                    element: resource,
                    source: resource.src || resource.href
                });
            });
        });
    }

    /**
     * Setup render error catching
     */
    setupRenderErrorCatching() {
        // Monitor for DOM mutations that might cause issues
        const observer = new MutationObserver((mutations) => {
            mutations.forEach((mutation) => {
                if (mutation.type === 'childList') {
                    mutation.addedNodes.forEach((node) => {
                        if (node.nodeType === Node.ELEMENT_NODE) {
                            this.validateNewElement(node);
                        }
                    });
                }
            });
        });

        observer.observe(this.element, {
            childList: true,
            subtree: true
        });

        this.mutationObserver = observer;
    }

    /**
     * Validate newly added elements
     */
    validateNewElement(element) {
        try {
            // Check for common issues
            if (element.tagName === 'SCRIPT') {
                this.validateScript(element);
            } else if (element.tagName === 'IMG') {
                this.validateImage(element);
            }
            
            // Check for accessibility issues
            this.validateAccessibility(element);
            
        } catch (error) {
            this.handleError({
                type: 'element_validation_error',
                message: `Element validation failed: ${error.message}`,
                error: error,
                element: element
            });
        }
    }

    /**
     * Validate script elements
     */
    validateScript(script) {
        if (script.src) {
            // Validate script source
            try {
                new URL(script.src);
            } catch (error) {
                throw new Error(`Invalid script URL: ${script.src}`);
            }
        }
    }

    /**
     * Validate image elements
     */
    validateImage(img) {
        if (img.src) {
            try {
                new URL(img.src);
            } catch (error) {
                throw new Error(`Invalid image URL: ${img.src}`);
            }
        }
        
        // Check for alt text (accessibility)
        if (!img.alt && !img.getAttribute('aria-label')) {
            console.warn('Image missing alt text:', img.src);
        }
    }

    /**
     * Validate accessibility
     */
    validateAccessibility(element) {
        // Basic accessibility checks
        if (element.hasAttribute('role')) {
            const role = element.getAttribute('role');
            const validRoles = ['button', 'link', 'heading', 'banner', 'navigation', 'main', 'complementary'];
            
            if (!validRoles.includes(role)) {
                console.warn(`Unknown ARIA role: ${role}`, element);
            }
        }

        // Check for interactive elements without proper attributes
        if (['button', 'a', 'input'].includes(element.tagName.toLowerCase())) {
            if (!element.getAttribute('aria-label') && !element.textContent.trim()) {
                console.warn('Interactive element missing accessible label:', element);
            }
        }
    }

    /**
     * Handle error within boundary
     */
    handleError(errorInfo) {
        this.errorCount++;
        this.lastError = errorInfo;
        
        // Log error if enabled
        if (this.options.logErrors) {
            console.error(`Error in boundary ${this.getBoundaryId()}:`, errorInfo);
        }

        // Track with analytics
        if (window.demoAnalytics) {
            window.demoAnalytics.trackError(errorInfo, {
                boundaryId: this.getBoundaryId(),
                errorCount: this.errorCount
            });
        }

        // Call custom error handler
        if (this.options.onError) {
            try {
                this.options.onError(errorInfo, this);
            } catch (handlerError) {
                console.error('Error handler failed:', handlerError);
            }
        }

        // Try recovery strategies
        this.attemptRecovery(errorInfo);
    }

    /**
     * Attempt error recovery
     */
    async attemptRecovery(errorInfo) {
        const recoveryStrategies = [
            () => this.retryOperation(errorInfo),
            () => this.reloadComponent(errorInfo),
            () => this.useCache(errorInfo),
            () => this.showFallback(errorInfo)
        ];

        for (const strategy of recoveryStrategies) {
            try {
                const result = await strategy();
                if (result.success) {
                    this.onRecoverySuccess(result);
                    return;
                }
            } catch (strategyError) {
                console.error('Recovery strategy failed:', strategyError);
            }
        }

        // All recovery strategies failed
        this.onRecoveryFailure(errorInfo);
    }

    /**
     * Retry the failed operation
     */
    async retryOperation(errorInfo) {
        if (!this.options.retryable || this.retryAttempts >= this.maxRetries) {
            return { success: false, reason: 'Max retries exceeded' };
        }

        this.retryAttempts++;
        
        // Show retry notification
        this.showRetryNotification(this.retryAttempts);
        
        // Wait with exponential backoff
        const delay = Math.min(1000 * Math.pow(2, this.retryAttempts - 1), 10000);
        await this.delay(delay);

        try {
            switch (errorInfo.type) {
                case 'fetch_error':
                    return await this.retryFetch(errorInfo);
                case 'script_load_error':
                    return await this.retryScriptLoad(errorInfo);
                case 'resource_error':
                    return await this.retryResourceLoad(errorInfo);
                default:
                    return await this.retryGeneric(errorInfo);
            }
        } catch (error) {
            return { success: false, error };
        }
    }

    /**
     * Retry fetch operation
     */
    async retryFetch(errorInfo) {
        try {
            const response = await fetch(errorInfo.url);
            if (response.ok) {
                return { success: true, response };
            }
            return { success: false, reason: 'Response not ok' };
        } catch (error) {
            return { success: false, error };
        }
    }

    /**
     * Retry script loading
     */
    async retryScriptLoad(errorInfo) {
        return new Promise((resolve) => {
            const script = document.createElement('script');
            script.src = errorInfo.source;
            
            script.onload = () => {
                resolve({ success: true });
            };
            
            script.onerror = () => {
                resolve({ success: false, reason: 'Script load failed' });
            };
            
            document.head.appendChild(script);
        });
    }

    /**
     * Retry resource loading
     */
    async retryResourceLoad(errorInfo) {
        if (errorInfo.element) {
            return new Promise((resolve) => {
                const element = errorInfo.element;
                
                element.onload = () => {
                    resolve({ success: true });
                };
                
                element.onerror = () => {
                    resolve({ success: false, reason: 'Resource load failed' });
                };
                
                // Retry loading
                const src = element.src || element.href;
                element.src = '';
                element.href = '';
                setTimeout(() => {
                    element.src = src;
                    element.href = src;
                }, 100);
            });
        }
        
        return { success: false, reason: 'No element to retry' };
    }

    /**
     * Generic retry
     */
    async retryGeneric(errorInfo) {
        // For generic errors, try reloading the component
        return this.reloadComponent(errorInfo);
    }

    /**
     * Reload component
     */
    async reloadComponent(errorInfo) {
        try {
            // Save current state
            const currentState = this.saveState();
            
            // Reset to original content
            this.element.innerHTML = this.originalContent;
            
            // Reinitialize
            this.initialize();
            
            // Restore state if possible
            this.restoreState(currentState);
            
            return { success: true, method: 'component_reload' };
        } catch (error) {
            return { success: false, error };
        }
    }

    /**
     * Use cached data
     */
    async useCache(errorInfo) {
        if (window.connectionManager) {
            const cachedData = window.connectionManager.getCachedResponse(errorInfo.url);
            if (cachedData) {
                return { success: true, method: 'cache', data: cachedData };
            }
        }
        
        return { success: false, reason: 'No cache available' };
    }

    /**
     * Show fallback UI
     */
    async showFallback(errorInfo) {
        this.isInErrorState = true;
        
        const fallbackHTML = this.generateFallbackHTML(errorInfo);
        this.element.innerHTML = fallbackHTML;
        
        // Add retry functionality
        this.setupFallbackActions();
        
        return { success: true, method: 'fallback' };
    }

    /**
     * Generate fallback HTML
     */
    generateFallbackHTML(errorInfo) {
        const boundaryId = this.getBoundaryId();
        
        return `
            <div class="error-boundary-fallback" data-boundary="${boundaryId}">
                <div class="error-boundary-content">
                    <div class="error-icon">⚠️</div>
                    <h3 class="error-title">Component Error</h3>
                    <p class="error-message">
                        ${this.getUserFriendlyMessage(errorInfo)}
                    </p>
                    <div class="error-details" style="display: none;">
                        <pre>${JSON.stringify(errorInfo, null, 2)}</pre>
                    </div>
                    <div class="error-actions">
                        <button class="retry-btn" onclick="window.ErrorBoundary.retry('${boundaryId}')">
                            Try Again
                        </button>
                        <button class="details-btn" onclick="window.ErrorBoundary.toggleDetails('${boundaryId}')">
                            Show Details
                        </button>
                        <button class="reset-btn" onclick="window.ErrorBoundary.reset('${boundaryId}')">
                            Reset Component
                        </button>
                    </div>
                </div>
            </div>
        `;
    }

    /**
     * Setup fallback actions
     */
    setupFallbackActions() {
        const boundaryId = this.getBoundaryId();
        
        // Register global actions
        if (!window.ErrorBoundary.actions) {
            window.ErrorBoundary.actions = {};
        }
        
        window.ErrorBoundary.actions[boundaryId] = {
            retry: () => this.retry(),
            toggleDetails: () => this.toggleDetails(),
            reset: () => this.reset()
        };
    }

    /**
     * Get user-friendly error message
     */
    getUserFriendlyMessage(errorInfo) {
        const messages = {
            'fetch_error': 'Unable to load data. Please check your connection.',
            'script_load_error': 'A required component failed to load.',
            'resource_error': 'Some content could not be displayed.',
            'promise_rejection': 'An operation failed unexpectedly.',
            'render_error': 'This component encountered a display issue.'
        };
        
        return messages[errorInfo.type] || 'An unexpected error occurred in this component.';
    }

    /**
     * Utility methods
     */
    getBoundaryId() {
        if (!this.boundaryId) {
            this.boundaryId = this.element.id || `boundary_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
        }
        return this.boundaryId;
    }

    addBoundaryMarker() {
        this.element.setAttribute('data-error-boundary', this.getBoundaryId());
        this.element.classList.add('error-boundary');
    }

    saveState() {
        // Save current state for recovery
        const inputs = this.element.querySelectorAll('input, select, textarea');
        const state = {};
        
        inputs.forEach(input => {
            if (input.id || input.name) {
                const key = input.id || input.name;
                state[key] = input.type === 'checkbox' ? input.checked : input.value;
            }
        });
        
        return state;
    }

    restoreState(state) {
        // Restore saved state
        Object.entries(state).forEach(([key, value]) => {
            const input = this.element.querySelector(`#${key}, [name="${key}"]`);
            if (input) {
                if (input.type === 'checkbox') {
                    input.checked = value;
                } else {
                    input.value = value;
                }
            }
        });
    }

    isPromiseFromBoundary(promise) {
        // This is a simplified check
        // In practice, you'd need more sophisticated tracking
        return true; // Assume all promises within boundary for now
    }

    delay(ms) {
        return new Promise(resolve => setTimeout(resolve, ms));
    }

    showRetryNotification(attempt) {
        if (window.errorHandler?.showNotification) {
            window.errorHandler.showNotification(
                'Retrying',
                `Attempting to recover... (${attempt}/${this.maxRetries})`,
                'info'
            );
        }
    }

    onRecoverySuccess(result) {
        this.isInErrorState = false;
        this.retryAttempts = 0;
        
        if (window.errorHandler?.showNotification) {
            window.errorHandler.showNotification(
                'Recovery Successful',
                `Component recovered using ${result.method}`,
                'success'
            );
        }
    }

    onRecoveryFailure(errorInfo) {
        this.isInErrorState = true;
        
        if (window.errorHandler?.showNotification) {
            window.errorHandler.showNotification(
                'Recovery Failed',
                'Component could not be recovered automatically',
                'error'
            );
        }
    }

    /**
     * Default error handler
     */
    defaultErrorHandler(errorInfo, boundary) {
        console.error(`Error in boundary ${boundary.getBoundaryId()}:`, errorInfo);
    }

    /**
     * Get default fallback component
     */
    getDefaultFallback() {
        return {
            template: this.generateFallbackHTML.bind(this),
            retryable: true
        };
    }

    /**
     * Public methods for fallback actions
     */
    retry() {
        this.retryAttempts = 0;
        this.attemptRecovery(this.lastError);
    }

    toggleDetails() {
        const details = this.element.querySelector('.error-details');
        if (details) {
            const isHidden = details.style.display === 'none';
            details.style.display = isHidden ? 'block' : 'none';
            
            const btn = this.element.querySelector('.details-btn');
            if (btn) {
                btn.textContent = isHidden ? 'Hide Details' : 'Show Details';
            }
        }
    }

    reset() {
        this.isInErrorState = false;
        this.errorCount = 0;
        this.retryAttempts = 0;
        this.lastError = null;
        
        // Restore original content
        this.element.innerHTML = this.originalContent;
        
        // Reinitialize
        this.initialize();
        
        if (window.errorHandler?.showNotification) {
            window.errorHandler.showNotification(
                'Component Reset',
                'Component has been reset to its original state',
                'info'
            );
        }
    }

    /**
     * Cleanup
     */
    destroy() {
        if (this.mutationObserver) {
            this.mutationObserver.disconnect();
        }
        
        // Remove from global registry
        const boundaryId = this.getBoundaryId();
        if (window.ErrorBoundary.actions?.[boundaryId]) {
            delete window.ErrorBoundary.actions[boundaryId];
        }
    }
}

// Static methods for ErrorBoundary class
ErrorBoundary.boundaries = new Map();

ErrorBoundary.create = function(selector, options = {}) {
    const elements = typeof selector === 'string' ? 
        document.querySelectorAll(selector) : [selector];
    
    const boundaries = [];
    
    elements.forEach(element => {
        const boundary = new ErrorBoundary(element, options);
        ErrorBoundary.boundaries.set(boundary.getBoundaryId(), boundary);
        boundaries.push(boundary);
    });
    
    return boundaries.length === 1 ? boundaries[0] : boundaries;
};

ErrorBoundary.findBoundaryForElement = function(element) {
    let current = element;
    while (current && current !== document.body) {
        const boundaryId = current.getAttribute('data-error-boundary');
        if (boundaryId) {
            return ErrorBoundary.boundaries.get(boundaryId);
        }
        current = current.parentElement;
    }
    return null;
};

ErrorBoundary.retry = function(boundaryId) {
    const action = ErrorBoundary.actions?.[boundaryId]?.retry;
    if (action) action();
};

ErrorBoundary.toggleDetails = function(boundaryId) {
    const action = ErrorBoundary.actions?.[boundaryId]?.toggleDetails;
    if (action) action();
};

ErrorBoundary.reset = function(boundaryId) {
    const action = ErrorBoundary.actions?.[boundaryId]?.reset;
    if (action) action();
};

// Global error boundary registry
window.ErrorBoundary = ErrorBoundary;

// Auto-create boundaries for elements with error-boundary class
document.addEventListener('DOMContentLoaded', () => {
    const boundaryElements = document.querySelectorAll('.error-boundary, [data-error-boundary]');
    boundaryElements.forEach(element => {
        if (!element.hasAttribute('data-error-boundary')) {
            ErrorBoundary.create(element);
        }
    });
});

// Export for module systems
if (typeof module !== 'undefined' && module.exports) {
    module.exports = ErrorBoundary;
}