# Design System Documentation

## Overview

The brianhardin.info website features a comprehensive design system built with CSS custom properties (CSS variables) that provides consistent styling, theming, and component architecture across the entire site.

## 🎨 Color System

### Primary Colors (Python-Inspired Blues)
```css
--color-primary-50: #eff6ff;   /* Lightest blue */
--color-primary-100: #dbeafe;  /* Light blue */
--color-primary-200: #bfdbfe;  /* Light blue */
--color-primary-300: #93c5fd;  /* Medium light blue */
--color-primary-400: #60a5fa;  /* Medium blue */
--color-primary-500: #3b82f6;  /* Main brand blue */
--color-primary-600: #2563eb;  /* Dark blue */
--color-primary-700: #1d4ed8;  /* Darker blue */
--color-primary-800: #1e40af;  /* Very dark blue */
--color-primary-900: #1e3a8a;  /* Darkest blue */
```

### Secondary Colors (Python Gold)
```css
--color-secondary-50: #fefce8;   /* Lightest gold */
--color-secondary-100: #fef9c3;  /* Light gold */
--color-secondary-500: #eab308;  /* Main gold */
--color-secondary-600: #ca8a04;  /* Dark gold */
--color-secondary-900: #713f12;  /* Darkest gold */
```

### Semantic Colors
```css
/* Success (Green) */
--color-success-50: #f0fdf4;
--color-success-500: #22c55e;
--color-success-600: #16a34a;

/* Warning (Orange) */
--color-warning-50: #fffbeb;
--color-warning-500: #f59e0b;
--color-warning-600: #d97706;

/* Error (Red) */
--color-error-50: #fef2f2;
--color-error-500: #ef4444;
--color-error-600: #dc2626;
```

### Neutral Grays
```css
--color-gray-50: #f8fafc;    /* Lightest gray */
--color-gray-100: #f1f5f9;   /* Very light gray */
--color-gray-200: #e2e8f0;   /* Light gray */
--color-gray-300: #cbd5e1;   /* Medium light gray */
--color-gray-400: #94a3b8;   /* Medium gray */
--color-gray-500: #64748b;   /* Base gray */
--color-gray-600: #475569;   /* Dark gray */
--color-gray-700: #334155;   /* Darker gray */
--color-gray-800: #1e293b;   /* Very dark gray */
--color-gray-900: #0f172a;   /* Darkest gray */
```

## 🔤 Typography System

### Font Families
```css
--font-sans: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
--font-mono: 'Fira Code', 'SF Mono', Monaco, 'Cascadia Code', 'Roboto Mono', monospace;
```

### Font Sizes
```css
--text-xs: 0.75rem;     /* 12px */
--text-sm: 0.875rem;    /* 14px */
--text-base: 1rem;      /* 16px */
--text-lg: 1.125rem;    /* 18px */
--text-xl: 1.25rem;     /* 20px */
--text-2xl: 1.5rem;     /* 24px */
--text-3xl: 1.875rem;   /* 30px */
--text-4xl: 2.25rem;    /* 36px */
--text-5xl: 3rem;       /* 48px */
--text-6xl: 3.75rem;    /* 60px */
--text-7xl: 4.5rem;     /* 72px */
```

### Font Weights
```css
--font-light: 300;
--font-normal: 400;
--font-medium: 500;
--font-semibold: 600;
--font-bold: 700;
--font-extrabold: 800;
```

### Line Heights
```css
--leading-tight: 1.25;
--leading-snug: 1.375;
--leading-normal: 1.5;
--leading-relaxed: 1.625;
--leading-loose: 2;
```

### Responsive Typography Classes
```css
.text-responsive-lg    /* Scales from text-2xl to text-4xl */
.text-responsive-xl    /* Scales from text-3xl to text-5xl */
.text-responsive-2xl   /* Scales from text-4xl to text-6xl */
.text-responsive-3xl   /* Scales from text-5xl to text-7xl */
```

## 📏 Spacing System

```css
--space-px: 1px;
--space-0: 0;
--space-1: 0.25rem;   /* 4px */
--space-2: 0.5rem;    /* 8px */
--space-3: 0.75rem;   /* 12px */
--space-4: 1rem;      /* 16px */
--space-5: 1.25rem;   /* 20px */
--space-6: 1.5rem;    /* 24px */
--space-8: 2rem;      /* 32px */
--space-10: 2.5rem;   /* 40px */
--space-12: 3rem;     /* 48px */
--space-16: 4rem;     /* 64px */
--space-20: 5rem;     /* 80px */
--space-24: 6rem;     /* 96px */
--space-32: 8rem;     /* 128px */
```

## 🌑 Dark Mode Support

The design system includes comprehensive dark mode support with automatic color inversion:

```css
.dark {
  /* Gray scale inversion for dark mode */
  --color-gray-50: #0f172a;
  --color-gray-100: #1e293b;
  --color-gray-200: #334155;
  --color-gray-300: #475569;
  --color-gray-400: #64748b;
  --color-gray-500: #94a3b8;
  --color-gray-600: #cbd5e1;
  --color-gray-700: #e2e8f0;
  --color-gray-800: #f1f5f9;
  --color-gray-900: #f8fafc;
}
```

### Semantic Color Classes
```css
.text-primary     /* Primary text color */
.text-muted       /* Muted text color */
.text-subtle      /* Subtle text color */
.text-inverse     /* Inverse text color */
```

## 🧩 Component Library

### Buttons
```css
.btn                /* Base button styles */
.btn-primary        /* Primary action button */
.btn-secondary      /* Secondary action button */
.btn.loading        /* Loading state with spinner */
```

**Usage:**
```html
<button class="btn-primary">Primary Action</button>
<button class="btn-secondary">Secondary Action</button>
<button class="btn-primary loading">Loading...</button>
```

### Cards
```css
.card               /* Base card component */
.interactive-card   /* Card with hover shimmer effect */
.feature-card       /* Feature showcase card */
.stats-card         /* Statistics display card */
```

**Usage:**
```html
<div class="card p-6 hover:shadow-xl">
  <h3>Card Title</h3>
  <p>Card content goes here...</p>
</div>
```

### Form Elements
```css
.form-group         /* Form field container */
.form-label         /* Form field label */
.form-input         /* Enhanced input field */
.form-help          /* Help text for fields */
.form-field-loading /* Loading state for fields */
```

**Usage:**
```html
<div class="form-group">
  <label class="form-label required">Email Address</label>
  <input type="email" class="form-input" placeholder="john@example.com">
  <div class="form-help">We'll never share your email</div>
</div>
```

### Badges and Status Indicators
```css
.badge              /* Base badge component */
.badge-primary      /* Primary colored badge */
.badge-success      /* Success state badge */
.badge-warning      /* Warning state badge */
.badge-error        /* Error state badge */

.status-indicator   /* Status indicator with dot */
.status-online      /* Online status (green) */
.status-busy        /* Busy status (orange) */
.status-offline     /* Offline status (gray) */
```

**Usage:**
```html
<span class="badge badge-primary">New</span>
<span class="badge badge-success">Published</span>

<div class="status-indicator status-online">
  Currently Available
</div>
```

### Progress Bars
```css
.progress-bar       /* Progress bar container */
.progress-fill      /* Progress bar fill */
.progress-indeterminate /* Indeterminate loading animation */
```

**Usage:**
```html
<div class="progress-bar">
  <div class="progress-fill" style="width: 75%"></div>
</div>
```

### Avatars
```css
.avatar             /* Base avatar component */
.avatar-sm          /* Small avatar (32px) */
.avatar-md          /* Medium avatar (40px) */
.avatar-lg          /* Large avatar (48px) */
.avatar-xl          /* Extra large avatar (64px) */
```

**Usage:**
```html
<div class="avatar avatar-lg">BH</div>
```

## 🎭 Animations and Effects

### Loading States
```css
.skeleton           /* Skeleton loading animation */
.pulse              /* Pulse animation */
.typing-indicator   /* Typing dots animation */
.spinner            /* Loading spinner */
```

### Hover Effects
```css
.hover-lift:hover   /* Lift effect on hover */
.hover-scale:hover  /* Scale effect on hover */
```

### Transitions
```css
--transition-fast: 150ms ease;
--transition-base: 200ms ease;
--transition-slow: 300ms ease;
--transition-slower: 500ms ease;
```

## 🏗 Layout Components

### Section Spacing
```css
.section            /* Standard section spacing */
.section-sm         /* Small section spacing */
.section-lg         /* Large section spacing */
```

### Container Widths
```css
.container          /* Standard container (1280px max) */
.container-sm       /* Small container (640px max) */
.container-lg       /* Large container (1536px max) */
```

### Utility Classes
```css
.divider            /* Horizontal divider line */
.divider-text       /* Divider with text */
```

## 📱 Responsive Breakpoints

The design system uses mobile-first responsive design:

```css
/* Mobile first (default) */
@media (min-width: 640px)  { /* sm */ }
@media (min-width: 768px)  { /* md */ }
@media (min-width: 1024px) { /* lg */ }
@media (min-width: 1280px) { /* xl */ }
```

## 🎨 Text Gradients

```css
.text-gradient-primary  /* Primary color gradient text */
```

**Usage:**
```html
<h1 class="text-gradient-primary">Gradient Heading</h1>
```

## 🔧 Implementation Best Practices

### 1. Use Design Tokens
Always use CSS custom properties instead of hard-coded values:

```css
/* ✅ Good */
.my-component {
  color: var(--color-primary-600);
  padding: var(--space-4);
  border-radius: var(--radius-lg);
}

/* ❌ Bad */
.my-component {
  color: #2563eb;
  padding: 16px;
  border-radius: 8px;
}
```

### 2. Follow Component Patterns
Use established component classes and extend them when needed:

```css
/* ✅ Good - Extending base component */
.my-special-card {
  @extend .card;
  border-left: 4px solid var(--color-primary-500);
}

/* ❌ Bad - Recreating from scratch */
.my-special-card {
  background: white;
  border-radius: 12px;
  box-shadow: 0 1px 3px rgba(0,0,0,0.1);
  /* ... recreating all card styles */
}
```

### 3. Maintain Dark Mode Compatibility
Always consider dark mode when creating new styles:

```css
.my-component {
  background: var(--color-gray-100);
  color: var(--color-gray-900);
}

.dark .my-component {
  background: var(--color-gray-800);
  color: var(--color-gray-100);
}
```

### 4. Use Semantic Color Names
Prefer semantic color utilities over specific color values:

```css
/* ✅ Good */
.error-message {
  color: var(--color-error-600);
}

/* ❌ Bad */
.error-message {
  color: var(--color-red-600);
}
```

## 🔍 Browser Support

The design system supports:
- **Modern Browsers**: Chrome 88+, Firefox 85+, Safari 14+, Edge 88+
- **CSS Features**: CSS Custom Properties, CSS Grid, Flexbox
- **Responsive**: Mobile-first design with progressive enhancement
- **Accessibility**: WCAG 2.1 AA compliant color contrast ratios

## 📚 Resources

- **Fonts**: [Inter](https://fonts.google.com/specimen/Inter), [Fira Code](https://fonts.google.com/specimen/Fira+Code)
- **Icons**: [Heroicons](https://heroicons.com/) (SVG icons used throughout)
- **Inspiration**: Python brand colors, modern web design principles
- **Testing**: Cross-browser compatibility tested with Puppeteer

---

This design system provides a solid foundation for consistent, maintainable, and accessible user interfaces across the brianhardin.info website.