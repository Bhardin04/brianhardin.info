/**
 * User Preferences and Demo State Management
 * Handles saving/loading user preferences and demo states
 */

class UserPreferencesManager {
    constructor() {
        this.storagePrefix = 'brianhardin_demo_';
        this.preferences = this.loadPreferences();
        this.demoStates = new Map();
        this.sessionData = new Map();
    }

    /**
     * Load user preferences from localStorage
     */
    loadPreferences() {
        try {
            const stored = localStorage.getItem(`${this.storagePrefix}preferences`);
            return stored ? JSON.parse(stored) : this.getDefaultPreferences();
        } catch (error) {
            console.error('Error loading preferences:', error);
            return this.getDefaultPreferences();
        }
    }

    /**
     * Get default preferences
     */
    getDefaultPreferences() {
        return {
            theme: 'auto', // 'light', 'dark', 'auto'
            exportFormat: 'pdf',
            chartAnimations: true,
            soundEffects: false,
            autoSave: true,
            defaultChartType: 'line',
            dataRefreshInterval: 30000, // 30 seconds
            notifications: {
                exports: true,
                errors: true,
                success: true,
                websocket: false
            },
            dashboard: {
                defaultPeriod: 'current_month',
                autoRefresh: false,
                showKPIs: true,
                compactMode: false
            },
            privacy: {
                analytics: true,
                errorReporting: true,
                usageStats: true
            }
        };
    }

    /**
     * Save preferences to localStorage
     */
    savePreferences() {
        try {
            localStorage.setItem(`${this.storagePrefix}preferences`, JSON.stringify(this.preferences));
            this.triggerPreferencesChange();
        } catch (error) {
            console.error('Error saving preferences:', error);
        }
    }

    /**
     * Get a preference value
     */
    getPreference(key, defaultValue = null) {
        const keys = key.split('.');
        let value = this.preferences;

        for (const k of keys) {
            if (value && typeof value === 'object' && k in value) {
                value = value[k];
            } else {
                return defaultValue;
            }
        }

        return value;
    }

    /**
     * Set a preference value
     */
    setPreference(key, value) {
        const keys = key.split('.');
        let current = this.preferences;

        for (let i = 0; i < keys.length - 1; i++) {
            const k = keys[i];
            if (!(k in current) || typeof current[k] !== 'object') {
                current[k] = {};
            }
            current = current[k];
        }

        current[keys[keys.length - 1]] = value;
        this.savePreferences();
    }

    /**
     * Save demo state
     */
    saveDemoState(demoType, sessionId, state) {
        const key = `${this.storagePrefix}state_${demoType}_${sessionId}`;
        const stateData = {
            ...state,
            timestamp: Date.now(),
            demoType: demoType,
            sessionId: sessionId
        };

        try {
            localStorage.setItem(key, JSON.stringify(stateData));
            this.demoStates.set(`${demoType}_${sessionId}`, stateData);
        } catch (error) {
            console.error('Error saving demo state:', error);
        }
    }

    /**
     * Load demo state
     */
    loadDemoState(demoType, sessionId) {
        const key = `${this.storagePrefix}state_${demoType}_${sessionId}`;

        try {
            const stored = localStorage.getItem(key);
            if (stored) {
                const state = JSON.parse(stored);
                this.demoStates.set(`${demoType}_${sessionId}`, state);
                return state;
            }
        } catch (error) {
            console.error('Error loading demo state:', error);
        }

        return null;
    }

    /**
     * Get all saved demo states
     */
    getAllDemoStates() {
        const states = [];

        for (let i = 0; i < localStorage.length; i++) {
            const key = localStorage.key(i);
            if (key && key.startsWith(`${this.storagePrefix}state_`)) {
                try {
                    const state = JSON.parse(localStorage.getItem(key));
                    states.push(state);
                } catch (error) {
                    console.error('Error parsing demo state:', error);
                }
            }
        }

        return states.sort((a, b) => b.timestamp - a.timestamp);
    }

    /**
     * Clear old demo states (older than 7 days)
     */
    clearOldStates() {
        const sevenDaysAgo = Date.now() - (7 * 24 * 60 * 60 * 1000);
        const keysToRemove = [];

        for (let i = 0; i < localStorage.length; i++) {
            const key = localStorage.key(i);
            if (key && key.startsWith(`${this.storagePrefix}state_`)) {
                try {
                    const state = JSON.parse(localStorage.getItem(key));
                    if (state.timestamp < sevenDaysAgo) {
                        keysToRemove.push(key);
                    }
                } catch (error) {
                    keysToRemove.push(key); // Remove corrupted entries
                }
            }
        }

        keysToRemove.forEach(key => {
            localStorage.removeItem(key);
        });

        console.log(`Cleared ${keysToRemove.length} old demo states`);
    }

    /**
     * Save session data (temporary, for current session only)
     */
    saveSessionData(key, data) {
        this.sessionData.set(key, {
            data: data,
            timestamp: Date.now()
        });
    }

    /**
     * Get session data
     */
    getSessionData(key) {
        const entry = this.sessionData.get(key);
        return entry ? entry.data : null;
    }

    /**
     * Clear session data
     */
    clearSessionData(key = null) {
        if (key) {
            this.sessionData.delete(key);
        } else {
            this.sessionData.clear();
        }
    }

    /**
     * Export user data
     */
    exportUserData() {
        const data = {
            preferences: this.preferences,
            demoStates: this.getAllDemoStates(),
            exportedAt: new Date().toISOString(),
            version: '1.0'
        };

        const blob = new Blob([JSON.stringify(data, null, 2)], {
            type: 'application/json'
        });

        const url = URL.createObjectURL(blob);
        const link = document.createElement('a');
        link.href = url;
        link.download = `demo_preferences_${new Date().toISOString().split('T')[0]}.json`;

        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);

        URL.revokeObjectURL(url);

        return data;
    }

    /**
     * Import user data
     */
    async importUserData(file) {
        return new Promise((resolve, reject) => {
            const reader = new FileReader();

            reader.onload = (e) => {
                try {
                    const data = JSON.parse(e.target.result);

                    if (data.preferences) {
                        this.preferences = { ...this.getDefaultPreferences(), ...data.preferences };
                        this.savePreferences();
                    }

                    if (data.demoStates && Array.isArray(data.demoStates)) {
                        data.demoStates.forEach(state => {
                            if (state.demoType && state.sessionId) {
                                this.saveDemoState(state.demoType, state.sessionId, state);
                            }
                        });
                    }

                    resolve(data);
                } catch (error) {
                    reject(new Error('Invalid data format'));
                }
            };

            reader.onerror = () => reject(new Error('File read error'));
            reader.readAsText(file);
        });
    }

    /**
     * Reset all preferences to defaults
     */
    resetPreferences() {
        this.preferences = this.getDefaultPreferences();
        this.savePreferences();
    }

    /**
     * Clear all data
     */
    clearAllData() {
        // Clear preferences
        localStorage.removeItem(`${this.storagePrefix}preferences`);

        // Clear demo states
        const keysToRemove = [];
        for (let i = 0; i < localStorage.length; i++) {
            const key = localStorage.key(i);
            if (key && key.startsWith(this.storagePrefix)) {
                keysToRemove.push(key);
            }
        }

        keysToRemove.forEach(key => {
            localStorage.removeItem(key);
        });

        // Clear session data
        this.sessionData.clear();
        this.demoStates.clear();

        // Reset to defaults
        this.preferences = this.getDefaultPreferences();
    }

    /**
     * Apply theme preference
     */
    applyTheme() {
        const theme = this.getPreference('theme', 'auto');
        const root = document.documentElement;

        if (theme === 'dark') {
            root.classList.add('dark');
        } else if (theme === 'light') {
            root.classList.remove('dark');
        } else {
            // Auto theme based on system preference
            const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
            if (prefersDark) {
                root.classList.add('dark');
            } else {
                root.classList.remove('dark');
            }
        }
    }

    /**
     * Trigger preferences change event
     */
    triggerPreferencesChange() {
        const event = new CustomEvent('preferencesChanged', {
            detail: {
                preferences: this.preferences
            }
        });
        document.dispatchEvent(event);
    }

    /**
     * Auto-save demo state periodically
     */
    startAutoSave(demoType, sessionId, getStateCallback) {
        if (!this.getPreference('autoSave', true)) return;

        const interval = setInterval(() => {
            if (typeof getStateCallback === 'function') {
                try {
                    const state = getStateCallback();
                    if (state) {
                        this.saveDemoState(demoType, sessionId, state);
                    }
                } catch (error) {
                    console.error('Auto-save error:', error);
                }
            }
        }, 30000); // Save every 30 seconds

        // Store interval reference for cleanup
        this.saveSessionData(`autoSave_${demoType}_${sessionId}`, interval);

        return interval;
    }

    /**
     * Stop auto-save
     */
    stopAutoSave(demoType, sessionId) {
        const interval = this.getSessionData(`autoSave_${demoType}_${sessionId}`);
        if (interval) {
            clearInterval(interval);
            this.clearSessionData(`autoSave_${demoType}_${sessionId}`);
        }
    }

    /**
     * Get usage statistics
     */
    getUsageStats() {
        const stats = {
            totalSessions: 0,
            demoUsage: {},
            exportCount: this.getSessionData('exportCount') || 0,
            lastUsed: null,
            favoriteDemo: null
        };

        const states = this.getAllDemoStates();
        stats.totalSessions = states.length;

        states.forEach(state => {
            if (!stats.demoUsage[state.demoType]) {
                stats.demoUsage[state.demoType] = 0;
            }
            stats.demoUsage[state.demoType]++;

            if (!stats.lastUsed || state.timestamp > stats.lastUsed) {
                stats.lastUsed = state.timestamp;
            }
        });

        // Find favorite demo
        let maxUsage = 0;
        Object.entries(stats.demoUsage).forEach(([demo, count]) => {
            if (count > maxUsage) {
                maxUsage = count;
                stats.favoriteDemo = demo;
            }
        });

        return stats;
    }

    /**
     * Track export usage
     */
    trackExport(format) {
        const currentCount = this.getSessionData('exportCount') || 0;
        this.saveSessionData('exportCount', currentCount + 1);

        const formatCount = this.getSessionData(`export_${format}`) || 0;
        this.saveSessionData(`export_${format}`, formatCount + 1);
    }
}

// CSS for preferences UI
const preferencesStyles = `
    .preferences-modal {
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: rgba(0, 0, 0, 0.5);
        display: flex;
        align-items: center;
        justify-content: center;
        z-index: 10000;
    }

    .preferences-content {
        background: white;
        border-radius: 0.5rem;
        box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.25);
        max-width: 600px;
        width: 90%;
        max-height: 80vh;
        overflow-y: auto;
        padding: 1.5rem;
    }

    .dark .preferences-content {
        background: #1f2937;
        color: white;
    }

    .preference-section {
        margin-bottom: 1.5rem;
        padding-bottom: 1rem;
        border-bottom: 1px solid #e5e7eb;
    }

    .dark .preference-section {
        border-bottom-color: #374151;
    }

    .preference-item {
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 0.75rem 0;
    }

    .preference-label {
        font-weight: 500;
        margin-bottom: 0.25rem;
    }

    .preference-description {
        font-size: 0.875rem;
        color: #6b7280;
    }

    .dark .preference-description {
        color: #9ca3af;
    }

    .preference-control {
        min-width: 120px;
        text-align: right;
    }

    .toggle-switch {
        position: relative;
        display: inline-block;
        width: 44px;
        height: 24px;
    }

    .toggle-switch input {
        opacity: 0;
        width: 0;
        height: 0;
    }

    .toggle-slider {
        position: absolute;
        cursor: pointer;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background-color: #ccc;
        transition: 0.3s;
        border-radius: 24px;
    }

    .toggle-slider:before {
        position: absolute;
        content: "";
        height: 18px;
        width: 18px;
        left: 3px;
        bottom: 3px;
        background-color: white;
        transition: 0.3s;
        border-radius: 50%;
    }

    input:checked + .toggle-slider {
        background-color: #3b82f6;
    }

    input:checked + .toggle-slider:before {
        transform: translateX(20px);
    }
`;

// Inject styles
if (!document.querySelector('#preferences-styles')) {
    const styleSheet = document.createElement('style');
    styleSheet.id = 'preferences-styles';
    styleSheet.textContent = preferencesStyles;
    document.head.appendChild(styleSheet);
}

// Global instance
window.userPreferences = new UserPreferencesManager();

// Initialize theme on load
document.addEventListener('DOMContentLoaded', () => {
    window.userPreferences.applyTheme();
    window.userPreferences.clearOldStates();
});

// Apply theme changes automatically
window.addEventListener('storage', (e) => {
    if (e.key && e.key.includes('preferences')) {
        window.userPreferences.loadPreferences();
        window.userPreferences.applyTheme();
    }
});

// System theme change detection
window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', () => {
    if (window.userPreferences.getPreference('theme') === 'auto') {
        window.userPreferences.applyTheme();
    }
});

// Export for module systems
if (typeof module !== 'undefined' && module.exports) {
    module.exports = UserPreferencesManager;
}
