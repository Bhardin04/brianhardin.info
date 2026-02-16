/**
 * Preferences UI Component
 * Provides a user interface for managing demo preferences
 */

class PreferencesUI {
    constructor(preferencesManager) {
        this.prefs = preferencesManager;
        this.modal = null;
        this.isOpen = false;
    }

    /**
     * Show preferences modal
     */
    show() {
        if (this.isOpen) return;

        this.createModal();
        this.isOpen = true;

        // Animate in
        requestAnimationFrame(() => {
            this.modal.style.opacity = '1';
        });
    }

    /**
     * Hide preferences modal
     */
    hide() {
        if (!this.isOpen || !this.modal) return;

        // Animate out
        this.modal.style.opacity = '0';

        setTimeout(() => {
            if (this.modal && this.modal.parentElement) {
                this.modal.parentElement.removeChild(this.modal);
            }
            this.modal = null;
            this.isOpen = false;
        }, 300);
    }

    /**
     * Create preferences modal
     */
    createModal() {
        this.modal = document.createElement('div');
        this.modal.className = 'preferences-modal';
        this.modal.style.opacity = '0';
        this.modal.style.transition = 'opacity 0.3s ease';

        this.modal.innerHTML = `
            <div class="preferences-content">
                <div class="flex items-center justify-between mb-6">
                    <h2 class="text-xl font-bold text-gray-900 dark:text-white">Demo Preferences</h2>
                    <button id="close-preferences" class="text-gray-400 hover:text-gray-600 dark:hover:text-gray-300">
                        <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
                        </svg>
                    </button>
                </div>

                <div class="space-y-6">
                    ${this.createAppearanceSection()}
                    ${this.createExportSection()}
                    ${this.createDashboardSection()}
                    ${this.createNotificationSection()}
                    ${this.createPrivacySection()}
                    ${this.createDataSection()}
                </div>

                <div class="flex justify-end gap-3 mt-8 pt-6 border-t border-gray-200 dark:border-gray-700">
                    <button id="reset-preferences" class="px-4 py-2 text-sm text-gray-600 dark:text-gray-300 hover:text-gray-800 dark:hover:text-white">
                        Reset to Defaults
                    </button>
                    <button id="export-preferences" class="px-4 py-2 text-sm bg-blue-600 text-white rounded hover:bg-blue-700">
                        Export Settings
                    </button>
                    <button id="save-preferences" class="px-4 py-2 text-sm bg-green-600 text-white rounded hover:bg-green-700">
                        Save
                    </button>
                </div>
            </div>
        `;

        document.body.appendChild(this.modal);
        this.attachEventListeners();
    }

    /**
     * Create appearance preferences section
     */
    createAppearanceSection() {
        const theme = this.prefs.getPreference('theme', 'auto');
        const animations = this.prefs.getPreference('chartAnimations', true);

        return `
            <div class="preference-section">
                <h3 class="text-lg font-semibold text-gray-900 dark:text-white mb-4">Appearance</h3>

                <div class="preference-item">
                    <div>
                        <div class="preference-label">Theme</div>
                        <div class="preference-description">Choose your preferred color scheme</div>
                    </div>
                    <div class="preference-control">
                        <select id="theme-select" class="rounded border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 px-3 py-1 text-sm">
                            <option value="auto" ${theme === 'auto' ? 'selected' : ''}>Auto</option>
                            <option value="light" ${theme === 'light' ? 'selected' : ''}>Light</option>
                            <option value="dark" ${theme === 'dark' ? 'selected' : ''}>Dark</option>
                        </select>
                    </div>
                </div>

                <div class="preference-item">
                    <div>
                        <div class="preference-label">Chart Animations</div>
                        <div class="preference-description">Enable smooth chart transitions</div>
                    </div>
                    <div class="preference-control">
                        <label class="toggle-switch">
                            <input type="checkbox" id="animations-toggle" ${animations ? 'checked' : ''}>
                            <span class="toggle-slider"></span>
                        </label>
                    </div>
                </div>
            </div>
        `;
    }

    /**
     * Create export preferences section
     */
    createExportSection() {
        const exportFormat = this.prefs.getPreference('exportFormat', 'pdf');

        return `
            <div class="preference-section">
                <h3 class="text-lg font-semibold text-gray-900 dark:text-white mb-4">Export Settings</h3>

                <div class="preference-item">
                    <div>
                        <div class="preference-label">Default Export Format</div>
                        <div class="preference-description">Preferred format for chart exports</div>
                    </div>
                    <div class="preference-control">
                        <select id="export-format-select" class="rounded border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 px-3 py-1 text-sm">
                            <option value="png" ${exportFormat === 'png' ? 'selected' : ''}>PNG Image</option>
                            <option value="pdf" ${exportFormat === 'pdf' ? 'selected' : ''}>PDF Document</option>
                            <option value="excel" ${exportFormat === 'excel' ? 'selected' : ''}>Excel File</option>
                            <option value="csv" ${exportFormat === 'csv' ? 'selected' : ''}>CSV Data</option>
                        </select>
                    </div>
                </div>
            </div>
        `;
    }

    /**
     * Create dashboard preferences section
     */
    createDashboardSection() {
        const defaultPeriod = this.prefs.getPreference('dashboard.defaultPeriod', 'current_month');
        const autoRefresh = this.prefs.getPreference('dashboard.autoRefresh', false);
        const showKPIs = this.prefs.getPreference('dashboard.showKPIs', true);
        const compactMode = this.prefs.getPreference('dashboard.compactMode', false);

        return `
            <div class="preference-section">
                <h3 class="text-lg font-semibold text-gray-900 dark:text-white mb-4">Dashboard</h3>

                <div class="preference-item">
                    <div>
                        <div class="preference-label">Default Time Period</div>
                        <div class="preference-description">Default period for dashboard data</div>
                    </div>
                    <div class="preference-control">
                        <select id="default-period-select" class="rounded border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 px-3 py-1 text-sm">
                            <option value="current_month" ${defaultPeriod === 'current_month' ? 'selected' : ''}>Current Month</option>
                            <option value="current_quarter" ${defaultPeriod === 'current_quarter' ? 'selected' : ''}>Current Quarter</option>
                            <option value="current_year" ${defaultPeriod === 'current_year' ? 'selected' : ''}>Current Year</option>
                        </select>
                    </div>
                </div>

                <div class="preference-item">
                    <div>
                        <div class="preference-label">Auto Refresh</div>
                        <div class="preference-description">Automatically refresh dashboard data</div>
                    </div>
                    <div class="preference-control">
                        <label class="toggle-switch">
                            <input type="checkbox" id="auto-refresh-toggle" ${autoRefresh ? 'checked' : ''}>
                            <span class="toggle-slider"></span>
                        </label>
                    </div>
                </div>

                <div class="preference-item">
                    <div>
                        <div class="preference-label">Show KPIs</div>
                        <div class="preference-description">Display key performance indicators</div>
                    </div>
                    <div class="preference-control">
                        <label class="toggle-switch">
                            <input type="checkbox" id="show-kpis-toggle" ${showKPIs ? 'checked' : ''}>
                            <span class="toggle-slider"></span>
                        </label>
                    </div>
                </div>

                <div class="preference-item">
                    <div>
                        <div class="preference-label">Compact Mode</div>
                        <div class="preference-description">Use compact layout for more data</div>
                    </div>
                    <div class="preference-control">
                        <label class="toggle-switch">
                            <input type="checkbox" id="compact-mode-toggle" ${compactMode ? 'checked' : ''}>
                            <span class="toggle-slider"></span>
                        </label>
                    </div>
                </div>
            </div>
        `;
    }

    /**
     * Create notification preferences section
     */
    createNotificationSection() {
        const exports = this.prefs.getPreference('notifications.exports', true);
        const errors = this.prefs.getPreference('notifications.errors', true);
        const success = this.prefs.getPreference('notifications.success', true);
        const websocket = this.prefs.getPreference('notifications.websocket', false);

        return `
            <div class="preference-section">
                <h3 class="text-lg font-semibold text-gray-900 dark:text-white mb-4">Notifications</h3>

                <div class="preference-item">
                    <div>
                        <div class="preference-label">Export Notifications</div>
                        <div class="preference-description">Show notifications for export operations</div>
                    </div>
                    <div class="preference-control">
                        <label class="toggle-switch">
                            <input type="checkbox" id="export-notifications-toggle" ${exports ? 'checked' : ''}>
                            <span class="toggle-slider"></span>
                        </label>
                    </div>
                </div>

                <div class="preference-item">
                    <div>
                        <div class="preference-label">Error Notifications</div>
                        <div class="preference-description">Show error messages and alerts</div>
                    </div>
                    <div class="preference-control">
                        <label class="toggle-switch">
                            <input type="checkbox" id="error-notifications-toggle" ${errors ? 'checked' : ''}>
                            <span class="toggle-slider"></span>
                        </label>
                    </div>
                </div>

                <div class="preference-item">
                    <div>
                        <div class="preference-label">Success Notifications</div>
                        <div class="preference-description">Show success confirmations</div>
                    </div>
                    <div class="preference-control">
                        <label class="toggle-switch">
                            <input type="checkbox" id="success-notifications-toggle" ${success ? 'checked' : ''}>
                            <span class="toggle-slider"></span>
                        </label>
                    </div>
                </div>

                <div class="preference-item">
                    <div>
                        <div class="preference-label">WebSocket Notifications</div>
                        <div class="preference-description">Show real-time connection status</div>
                    </div>
                    <div class="preference-control">
                        <label class="toggle-switch">
                            <input type="checkbox" id="websocket-notifications-toggle" ${websocket ? 'checked' : ''}>
                            <span class="toggle-slider"></span>
                        </label>
                    </div>
                </div>
            </div>
        `;
    }

    /**
     * Create privacy preferences section
     */
    createPrivacySection() {
        const analytics = this.prefs.getPreference('privacy.analytics', true);
        const errorReporting = this.prefs.getPreference('privacy.errorReporting', true);
        const usageStats = this.prefs.getPreference('privacy.usageStats', true);

        return `
            <div class="preference-section">
                <h3 class="text-lg font-semibold text-gray-900 dark:text-white mb-4">Privacy</h3>

                <div class="preference-item">
                    <div>
                        <div class="preference-label">Analytics</div>
                        <div class="preference-description">Allow anonymous usage analytics</div>
                    </div>
                    <div class="preference-control">
                        <label class="toggle-switch">
                            <input type="checkbox" id="analytics-toggle" ${analytics ? 'checked' : ''}>
                            <span class="toggle-slider"></span>
                        </label>
                    </div>
                </div>

                <div class="preference-item">
                    <div>
                        <div class="preference-label">Error Reporting</div>
                        <div class="preference-description">Send error reports to improve the experience</div>
                    </div>
                    <div class="preference-control">
                        <label class="toggle-switch">
                            <input type="checkbox" id="error-reporting-toggle" ${errorReporting ? 'checked' : ''}>
                            <span class="toggle-slider"></span>
                        </label>
                    </div>
                </div>

                <div class="preference-item">
                    <div>
                        <div class="preference-label">Usage Statistics</div>
                        <div class="preference-description">Track demo usage for improvements</div>
                    </div>
                    <div class="preference-control">
                        <label class="toggle-switch">
                            <input type="checkbox" id="usage-stats-toggle" ${usageStats ? 'checked' : ''}>
                            <span class="toggle-slider"></span>
                        </label>
                    </div>
                </div>
            </div>
        `;
    }

    /**
     * Create data management section
     */
    createDataSection() {
        const autoSave = this.prefs.getPreference('autoSave', true);
        const stats = this.prefs.getUsageStats();

        return `
            <div class="preference-section">
                <h3 class="text-lg font-semibold text-gray-900 dark:text-white mb-4">Data Management</h3>

                <div class="preference-item">
                    <div>
                        <div class="preference-label">Auto-Save Demo State</div>
                        <div class="preference-description">Automatically save your demo progress</div>
                    </div>
                    <div class="preference-control">
                        <label class="toggle-switch">
                            <input type="checkbox" id="auto-save-toggle" ${autoSave ? 'checked' : ''}>
                            <span class="toggle-slider"></span>
                        </label>
                    </div>
                </div>

                <div class="bg-gray-50 dark:bg-gray-800 rounded-lg p-4 mt-4">
                    <h4 class="text-sm font-medium text-gray-900 dark:text-white mb-3">Usage Statistics</h4>
                    <div class="grid grid-cols-2 gap-4 text-sm">
                        <div>
                            <span class="text-gray-600 dark:text-gray-300">Total Sessions:</span>
                            <span class="font-medium text-gray-900 dark:text-white ml-2">${stats.totalSessions}</span>
                        </div>
                        <div>
                            <span class="text-gray-600 dark:text-gray-300">Exports:</span>
                            <span class="font-medium text-gray-900 dark:text-white ml-2">${stats.exportCount}</span>
                        </div>
                        ${stats.favoriteDemo ? `
                        <div class="col-span-2">
                            <span class="text-gray-600 dark:text-gray-300">Most Used Demo:</span>
                            <span class="font-medium text-gray-900 dark:text-white ml-2">${stats.favoriteDemo.replace('_', ' ').replace(/\\b\\w/g, l => l.toUpperCase())}</span>
                        </div>
                        ` : ''}
                    </div>
                </div>

                <div class="mt-4 space-y-2">
                    <button id="clear-demo-states" class="w-full text-left px-4 py-2 text-sm bg-yellow-50 dark:bg-yellow-900/20 text-yellow-800 dark:text-yellow-200 rounded hover:bg-yellow-100 dark:hover:bg-yellow-900/30">
                        Clear All Saved Demo States
                    </button>
                    <button id="import-preferences" class="w-full text-left px-4 py-2 text-sm bg-blue-50 dark:bg-blue-900/20 text-blue-800 dark:text-blue-200 rounded hover:bg-blue-100 dark:hover:bg-blue-900/30">
                        Import Settings from File
                    </button>
                </div>
            </div>
        `;
    }

    /**
     * Attach event listeners to modal elements
     */
    attachEventListeners() {
        // Close modal
        this.modal.querySelector('#close-preferences').addEventListener('click', () => {
            this.hide();
        });

        // Click outside to close
        this.modal.addEventListener('click', (e) => {
            if (e.target === this.modal) {
                this.hide();
            }
        });

        // Save preferences
        this.modal.querySelector('#save-preferences').addEventListener('click', () => {
            this.savePreferences();
            this.hide();
        });

        // Reset preferences
        this.modal.querySelector('#reset-preferences').addEventListener('click', () => {
            if (confirm('Reset all preferences to defaults? This cannot be undone.')) {
                this.prefs.resetPreferences();
                this.hide();
                setTimeout(() => location.reload(), 100);
            }
        });

        // Export preferences
        this.modal.querySelector('#export-preferences').addEventListener('click', () => {
            this.prefs.exportUserData();
        });

        // Clear demo states
        this.modal.querySelector('#clear-demo-states').addEventListener('click', () => {
            if (confirm('Clear all saved demo states? This cannot be undone.')) {
                this.prefs.clearAllData();
                alert('Demo states cleared successfully');
            }
        });

        // Import preferences
        this.modal.querySelector('#import-preferences').addEventListener('click', () => {
            const input = document.createElement('input');
            input.type = 'file';
            input.accept = '.json';
            input.onchange = async (e) => {
                const file = e.target.files[0];
                if (file) {
                    try {
                        await this.prefs.importUserData(file);
                        alert('Settings imported successfully');
                        this.hide();
                        setTimeout(() => location.reload(), 100);
                    } catch (error) {
                        alert('Error importing settings: ' + error.message);
                    }
                }
            };
            input.click();
        });
    }

    /**
     * Save all preferences from the modal
     */
    savePreferences() {
        // Theme
        const theme = this.modal.querySelector('#theme-select').value;
        this.prefs.setPreference('theme', theme);

        // Animations
        const animations = this.modal.querySelector('#animations-toggle').checked;
        this.prefs.setPreference('chartAnimations', animations);

        // Export format
        const exportFormat = this.modal.querySelector('#export-format-select').value;
        this.prefs.setPreference('exportFormat', exportFormat);

        // Dashboard preferences
        const defaultPeriod = this.modal.querySelector('#default-period-select').value;
        this.prefs.setPreference('dashboard.defaultPeriod', defaultPeriod);

        const autoRefresh = this.modal.querySelector('#auto-refresh-toggle').checked;
        this.prefs.setPreference('dashboard.autoRefresh', autoRefresh);

        const showKPIs = this.modal.querySelector('#show-kpis-toggle').checked;
        this.prefs.setPreference('dashboard.showKPIs', showKPIs);

        const compactMode = this.modal.querySelector('#compact-mode-toggle').checked;
        this.prefs.setPreference('dashboard.compactMode', compactMode);

        // Notifications
        const exportNotifications = this.modal.querySelector('#export-notifications-toggle').checked;
        this.prefs.setPreference('notifications.exports', exportNotifications);

        const errorNotifications = this.modal.querySelector('#error-notifications-toggle').checked;
        this.prefs.setPreference('notifications.errors', errorNotifications);

        const successNotifications = this.modal.querySelector('#success-notifications-toggle').checked;
        this.prefs.setPreference('notifications.success', successNotifications);

        const websocketNotifications = this.modal.querySelector('#websocket-notifications-toggle').checked;
        this.prefs.setPreference('notifications.websocket', websocketNotifications);

        // Privacy
        const analytics = this.modal.querySelector('#analytics-toggle').checked;
        this.prefs.setPreference('privacy.analytics', analytics);

        const errorReporting = this.modal.querySelector('#error-reporting-toggle').checked;
        this.prefs.setPreference('privacy.errorReporting', errorReporting);

        const usageStats = this.modal.querySelector('#usage-stats-toggle').checked;
        this.prefs.setPreference('privacy.usageStats', usageStats);

        // Auto-save
        const autoSave = this.modal.querySelector('#auto-save-toggle').checked;
        this.prefs.setPreference('autoSave', autoSave);

        // Apply theme immediately
        this.prefs.applyTheme();
    }
}

// Global instance
window.preferencesUI = null;

// Initialize when preferences manager is available
document.addEventListener('DOMContentLoaded', () => {
    if (window.userPreferences) {
        window.preferencesUI = new PreferencesUI(window.userPreferences);
    }
});

// Export for module systems
if (typeof module !== 'undefined' && module.exports) {
    module.exports = PreferencesUI;
}
