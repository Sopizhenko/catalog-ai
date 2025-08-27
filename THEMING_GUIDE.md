# Catalog AI - Theming & Design System Reference

> **Version**: 1.0  
> **Last Updated**: December 2024  
> **Application**: Catalog AI (React + Flask)

## Table of Contents
1. [Overview](#overview)
2. [Brand Identity](#brand-identity)
3. [Color Palette](#color-palette)
4. [Typography](#typography)
5. [Spacing & Layout](#spacing--layout)
6. [Components](#components)
7. [Animations](#animations)
8. [Responsive Design](#responsive-design)
9. [Accessibility](#accessibility)
10. [Development Guidelines](#development-guidelines)

## Overview

The Catalog AI application uses a comprehensive CSS custom properties-based design system that ensures visual consistency, maintainability, and accessibility. The theme is built around the **Confirma Software** brand identity with a modern, clean aesthetic.

### Core Principles
- **Consistency**: All components use standardized design tokens
- **Accessibility**: WCAG compliant colors and focus states
- **Modularity**: Reusable CSS custom properties and component classes
- **Performance**: Optimized animations and efficient CSS architecture
- **Responsive**: Mobile-first design approach

---

## Brand Identity

### Primary Brand
- **Company**: Confirma Software
- **Primary Color**: `#009607` (Confirma Green)
- **Font Family**: Sofia Pro (custom font family)
- **Design Style**: Modern, professional, clean with subtle rounded corners

### Visual Language
- **Borders**: Sharp edges (border-radius: 0 for most elements)
- **Shadows**: Soft, layered shadows using CSS custom properties
- **Gradients**: Subtle brand-colored gradients for emphasis
- **Icons**: Lucide React icon library for consistency

---

## Color Palette

All colors are defined as CSS custom properties in `:root` for easy maintenance.

### Primary Colors (Confirma Brand Green)
```css
--primary-50: #f0fdf4;     /* Lightest tint */
--primary-100: #dcfce7;
--primary-200: #bbf7d0;
--primary-300: #86efac;
--primary-400: #4ade80;
--primary-500: #009607;     /* Base brand color */
--primary-600: #008005;
--primary-700: #006a04;
--primary-800: #005503;
--primary-900: #004002;     /* Darkest shade */
--primary-brand: #009607;   /* Alias for primary-500 */
```

### Secondary Colors (Professional Gray)
```css
--secondary-50: #f8fafc;    /* Background tints */
--secondary-100: #f1f5f9;
--secondary-200: #e2e8f0;
--secondary-300: #cbd5e1;
--secondary-400: #94a3b8;
--secondary-500: #64748b;   /* Mid-gray */
--secondary-600: #475569;
--secondary-700: #334155;
--secondary-800: #1e293b;   /* Primary text */
--secondary-900: #0f172a;   /* Darkest text */
```

### Accent Colors (Nordic Blue)
```css
--accent-50: #eff6ff;
--accent-100: #dbeafe;
--accent-200: #bfdbfe;
--accent-300: #93c5fd;
--accent-400: #60a5fa;
--accent-500: #3b82f6;      /* Base accent */
--accent-600: #2563eb;
--accent-700: #1d4ed8;
--accent-800: #1e40af;
--accent-900: #1e3a8a;
```

### Semantic Colors
```css
--success: var(--primary-brand);  /* Green */
--warning: #f59e0b;               /* Amber */
--error: #ef4444;                 /* Red */
--info: var(--primary-brand);     /* Green */
```

### Neutral Colors
```css
--white: #ffffff;
--gray-50: #f9fafb;          /* Lightest gray */
--gray-100: #f3f4f6;
--gray-200: #e5e7eb;
--gray-300: #d1d5db;
--gray-400: #9ca3af;
--gray-500: #6b7280;
--gray-600: #4b5563;
--gray-700: #374151;
--gray-800: #1f2937;
--gray-900: #111827;         /* Darkest gray */
```

### Usage Guidelines

**Primary Colors**: Use for call-to-action buttons, active states, brand elements
**Secondary Colors**: Use for text, borders, backgrounds, neutral elements  
**Accent Colors**: Use for highlights, secondary actions, informational elements
**Semantic Colors**: Use for success/warning/error states with appropriate meaning

---

## Typography

### Font Family
```css
--font-family-sans: "Sofia Pro", "Inter", -apple-system, BlinkMacSystemFont, "Segoe UI", "Roboto", "Oxygen", "Ubuntu", "Cantarell", "Fira Sans", "Droid Sans", "Helvetica Neue", sans-serif;
--font-family-mono: "JetBrains Mono", "Fira Code", "Monaco", "Consolas", monospace;
```

### Sofia Pro Font Weights Available
- **Light**: 300 (`--font-light`)
- **Normal**: 400 (`--font-normal`)
- **Medium**: 500 (`--font-medium`)
- **Semi Bold**: 600 (`--font-semibold`)
- **Bold**: 700 (`--font-bold`)
- **Extra Bold**: 800 (`--font-extrabold`)
- **Black**: 900 (used for large brand letters)

### Font Sizes
```css
--text-xs: 0.75rem;    /* 12px */
--text-sm: 0.875rem;   /* 14px */
--text-base: 1rem;     /* 16px - Base size */
--text-lg: 1.125rem;   /* 18px */
--text-xl: 1.25rem;    /* 20px */
--text-2xl: 1.5rem;    /* 24px */
--text-3xl: 1.875rem;  /* 30px */
--text-4xl: 2.25rem;   /* 36px */
--text-5xl: 3rem;      /* 48px */
--text-6xl: 3.75rem;   /* 60px */
```

### Line Heights
```css
--leading-tight: 1.25;
--leading-snug: 1.375;
--leading-normal: 1.5;     /* Default */
--leading-relaxed: 1.625;
--leading-loose: 2;
```

### Typography Hierarchy
- **H1 (Headers)**: `--text-5xl`, `--font-bold`, `--secondary-800`
- **H2 (Section titles)**: `--text-2xl`, `--font-bold`, `--secondary-800`  
- **H3 (Card titles)**: `--text-xl`, `--font-bold`, `--secondary-800`
- **Body Text**: `--text-base`, `--font-normal`, `--secondary-600`
- **Small Text**: `--text-sm`, `--font-medium`, `--secondary-500`
- **Labels**: `--text-sm`, `--font-semibold`, `--secondary-700`

---

## Spacing & Layout

### Spacing Scale
```css
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
```

### Border Radius (Confirma Style - Minimal)
```css
--radius-sm: 0;     /* Sharp edges */
--radius-md: 0;     /* Sharp edges */
--radius-lg: 0;     /* Sharp edges */
--radius-xl: 0;     /* Sharp edges */
--radius-2xl: 0;    /* Sharp edges */
--radius-3xl: 0;    /* Sharp edges */  
--radius-full: 0;   /* Sharp edges */
```
> **Note**: Confirma brand uses sharp edges. Only exceptions are pill-shaped elements like badges and tags.

### Shadows
```css
--shadow-sm: 0 1px 3px 0 rgb(0 0 0 / 0.1), 0 1px 2px -1px rgb(0 0 0 / 0.1);
--shadow-md: 0 4px 6px -1px rgb(0 0 0 / 0.1), 0 2px 4px -2px rgb(0 0 0 / 0.1);
--shadow-lg: 0 10px 15px -3px rgb(0 0 0 / 0.1), 0 4px 6px -4px rgb(0 0 0 / 0.1);
--shadow-xl: 0 20px 25px -5px rgb(0 0 0 / 0.1), 0 8px 10px -6px rgb(0 0 0 / 0.1);
--shadow-2xl: 0 25px 50px -12px rgb(0 0 0 / 0.25);
--shadow-inner: inset 0 2px 4px 0 rgb(0 0 0 / 0.05);
```

### Layout Containers
- **Max Width**: 1200px for main content
- **Grid Columns**: 3 columns on desktop, 2 on tablet, 1 on mobile
- **Grid Gap**: `var(--space-6)` (24px) on desktop, `var(--space-4)` (16px) on mobile

---

## Components

### Cards
**Base Class**: `.product-card`, `.company-card`

```css
/* Standard card styling */
background: var(--white);
border-radius: var(--radius-2xl);
padding: var(--space-8);
box-shadow: var(--shadow-lg);
border: 1px solid var(--secondary-200);
transition: var(--transition-normal);

/* Hover state */
transform: translateY(-4px);
box-shadow: var(--shadow-2xl);

/* Top border accent */
::before {
  height: 4px;
  background: linear-gradient(135deg, var(--primary-brand), var(--primary-700));
}
```

### Buttons

#### Primary Button
```css
.expand-btn, .contact-button {
  background: linear-gradient(135deg, var(--primary-brand), var(--primary-700));
  color: var(--white);
  padding: var(--space-4) var(--space-6);
  border-radius: var(--radius-full);
  font-weight: var(--font-semibold);
  transition: var(--transition-normal);
}
```

#### Filter Button
```css
.filter-btn {
  background: var(--white);
  border: 2px solid var(--secondary-200);
  border-radius: var(--radius-full);
  color: var(--secondary-700);
  
  /* Active state */
  &.active {
    background: var(--primary-brand);
    border-color: var(--primary-brand);
    color: var(--white);
  }
}
```

### Tags & Badges

#### Category Badge
```css
.product-category {
  background: var(--accent-100);
  color: var(--accent-700);
  padding: var(--space-1) var(--space-3);
  border-radius: var(--radius-full);
  font-size: var(--text-xs);
  font-weight: var(--font-semibold);
}
```

#### Feature Tag
```css
.feature-tag {
  background: var(--accent-50);
  color: var(--accent-700);
  padding: var(--space-1) var(--space-2);
  border: 1px solid var(--accent-200);
  font-size: var(--text-xs);
  font-weight: var(--font-medium);
}
```

#### Company Badge
```css
.company-badge {
  background: var(--primary-100);
  color: var(--primary-700);
  padding: var(--space-1) var(--space-3);
  border-radius: var(--radius-full);
  font-size: var(--text-xs);
  font-weight: var(--font-semibold);
}
```

### Forms

#### Input Fields
```css
.search-bar, .search-input {
  padding: var(--space-4) var(--space-5);
  border: 2px solid var(--secondary-300);
  border-radius: var(--radius-full);
  background: var(--white);
  font-size: var(--text-base);
  
  /* Focus state */
  &:focus {
    border-color: var(--primary-500);
    box-shadow: 0 0 0 3px rgba(0, 150, 7, 0.1);
    outline: none;
  }
}
```

### Modal
```css
.modal {
  background: rgba(0, 0, 0, 0.5);
  backdrop-filter: blur(4px);
  z-index: var(--z-modal);
}

.modal-content {
  background: var(--white);
  border-radius: var(--radius-2xl);
  box-shadow: var(--shadow-2xl);
  border: 1px solid var(--secondary-200);
}

.modal-header {
  background: linear-gradient(135deg, var(--primary-600), var(--primary-800));
  color: var(--white);
  padding: var(--space-8);
}
```

---

## Animations

### Transitions
```css
--transition-fast: 150ms ease-in-out;
--transition-normal: 250ms ease-in-out;
--transition-slow: 350ms ease-in-out;
```

### Key Animation Classes
```css
/* Fade in */
.animate-fade-in {
  animation: fadeIn 0.25s ease-out forwards;
}

/* Card entrance */
.animate-card-enter {
  animation: cardEnter 0.25s cubic-bezier(0.25, 0.46, 0.45, 0.94) forwards;
}

/* Slide up */
.animate-slide-up {
  animation: slideUp 0.25s cubic-bezier(0.25, 0.46, 0.45, 0.94) forwards;
}
```

### Hover Effects
- **Cards**: `translateY(-8px) scale(1.02)` with enhanced shadow
- **Buttons**: `translateY(-2px)` with color darkening
- **Tags**: `scale(1.05)` with color change

### Animation Performance
- Uses `will-change: transform, opacity` for optimized animations
- Respects `prefers-reduced-motion: reduce` for accessibility
- Staggered delays for grid item animations

---

## Responsive Design

### Breakpoints
```css
/* Tablet */
@media (max-width: 1024px) {
  /* 2-column grid */
}

/* Mobile */
@media (max-width: 768px) {
  /* Single column, adjusted spacing */
}

/* Small mobile */
@media (max-width: 480px) {
  /* Compact spacing, smaller text */
}
```

### Responsive Patterns
- **Grid**: 3 cols → 2 cols → 1 col
- **Typography**: Smaller heading sizes on mobile
- **Spacing**: Reduced padding/margins on mobile
- **Navigation**: Stacked navigation on small screens

---

## Accessibility

### Focus States
```css
.filter-btn:focus,
.search-bar:focus,
.back-button:focus,
.expand-btn:focus {
  outline: 2px solid var(--primary-500);
  outline-offset: 2px;
}
```

### High Contrast Support
```css
@media (prefers-contrast: high) {
  :root {
    --primary-500: #1d4ed8;
    --secondary-800: #000000;
    --secondary-600: #333333;
  }
}
```

### Color Contrast Requirements
- **Text on white**: Use `--secondary-700` or darker
- **White text**: Only on `--primary-600` or darker backgrounds
- **Interactive elements**: Minimum 3:1 contrast ratio
- **Focus indicators**: High contrast, clearly visible

---

## Development Guidelines

### CSS Custom Properties Usage

#### ✅ DO
```css
/* Use design tokens */
.my-component {
  color: var(--secondary-800);
  padding: var(--space-4);
  border-radius: var(--radius-lg);
  transition: var(--transition-normal);
}

/* Use semantic color names */
.success-state {
  color: var(--success);
}
```

#### ❌ DON'T
```css
/* Don't use hardcoded values */
.my-component {
  color: #1e293b;
  padding: 16px;
  border-radius: 8px;
  transition: 250ms ease-in-out;
}

/* Don't use hex codes directly */
.error-state {
  color: #ef4444;
}
```

### Component Naming Convention

#### Pattern: `.component-name`
- `.product-card`
- `.company-selector`  
- `.search-container`
- `.filter-btn`
- `.modal-header`

#### Element Pattern: `.component__element`
- `.product-card__header`
- `.product-card__description`
- `.company-selector__dropdown`

#### Modifier Pattern: `.component--modifier`
- `.product-card--selected`
- `.filter-btn--active`
- `.modal--large`

### File Organization
```
frontend/src/styles/
├── index.css           # Main stylesheet with all tokens and components
├── components/         # Individual component styles (if needed)
└── utilities/          # Utility classes (if needed)
```

### Adding New Colors

1. **Define in `:root`** with proper naming convention
2. **Follow the scale pattern** (50, 100, 200...900)
3. **Test contrast ratios** for accessibility
4. **Document the usage** in this guide

Example:
```css
:root {
  /* New color scale */
  --tertiary-50: #fefefe;
  --tertiary-100: #fdfdfd;
  /* ... continue the scale */
  --tertiary-900: #0a0a0a;
}
```

### Adding New Components

1. **Use existing design tokens** where possible
2. **Follow established patterns** for hover states, transitions
3. **Include responsive behavior**
4. **Test accessibility** (focus states, contrast)
5. **Document new patterns** in this guide

### Performance Considerations

- **Use `transform` and `opacity`** for animations (GPU accelerated)
- **Avoid animating** `width`, `height`, `padding` (causes layout thrashing)
- **Use `will-change`** sparingly and remove after animation
- **Optimize shadows** - use fewer, simpler shadows when possible

---

## Version History

### v1.0 (December 2024)
- Initial theming system documentation
- Complete color palette with Confirma branding
- Typography system with Sofia Pro
- Component library documentation
- Responsive design guidelines
- Accessibility standards
- Animation framework

---

## Support & Updates

For questions or updates to this design system:

1. **Review existing patterns** before creating new ones
2. **Test changes** across all breakpoints and browsers
3. **Validate accessibility** with screen readers and contrast tools
4. **Update this documentation** when making changes
5. **Consider design system impact** - changes affect the entire application

---

*This guide serves as the single source of truth for theming and visual design in the Catalog AI application. Always refer to this document when implementing new features or modifying existing ones.*
