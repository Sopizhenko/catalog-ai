# CSS Variables Cheat Sheet - Catalog AI

## 🎨 Colors

### Primary (Brand Green)
```css
var(--primary-brand)    /* #009607 - Main brand */
var(--primary-50)       /* #f0fdf4 - Lightest */
var(--primary-100)      /* #dcfce7 - Backgrounds */
var(--primary-600)      /* #008005 - Buttons */
var(--primary-700)      /* #006a04 - Hover states */
```

### Text & Backgrounds
```css
var(--white)            /* #ffffff */
var(--secondary-800)    /* #1e293b - Primary text */
var(--secondary-600)    /* #475569 - Secondary text */
var(--secondary-500)    /* #64748b - Muted text */
var(--secondary-300)    /* #cbd5e1 - Borders */
var(--secondary-200)    /* #e2e8f0 - Light borders */
var(--secondary-100)    /* #f1f5f9 - Subtle bg */
var(--secondary-50)     /* #f8fafc - Page bg */
```

### Accents (Blue)
```css
var(--accent-600)       /* #2563eb */
var(--accent-100)       /* #dbeafe */
```

### Semantic
```css
var(--success)          /* Same as primary-brand */
var(--warning)          /* #f59e0b */
var(--error)            /* #ef4444 */
```

## 📏 Spacing
```css
var(--space-1)          /* 4px */
var(--space-2)          /* 8px */
var(--space-3)          /* 12px */
var(--space-4)          /* 16px */
var(--space-5)          /* 20px */
var(--space-6)          /* 24px */
var(--space-8)          /* 32px */
var(--space-10)         /* 40px */
var(--space-12)         /* 48px */
var(--space-16)         /* 64px */
```

## 🔤 Typography
```css
var(--font-family-sans)  /* Sofia Pro + fallbacks */
var(--text-xs)          /* 12px */
var(--text-sm)          /* 14px */
var(--text-base)        /* 16px */
var(--text-lg)          /* 18px */
var(--text-xl)          /* 20px */
var(--text-2xl)         /* 24px */
var(--text-3xl)         /* 30px */
var(--text-4xl)         /* 36px */
var(--text-5xl)         /* 48px */

var(--font-normal)      /* 400 */
var(--font-medium)      /* 500 */
var(--font-semibold)    /* 600 */
var(--font-bold)        /* 700 */
```

## 🌟 Effects
```css
var(--shadow-sm)        /* Subtle shadow */
var(--shadow-md)        /* Medium shadow */
var(--shadow-lg)        /* Card shadow */
var(--shadow-xl)        /* Large shadow */
var(--shadow-2xl)       /* Modal shadow */

var(--transition-fast)   /* 150ms */
var(--transition-normal) /* 250ms */
var(--transition-slow)   /* 350ms */

var(--radius-full)      /* For pills/badges only */
/* Note: Most elements use sharp edges (radius: 0) */
```

## 📱 Z-Index
```css
var(--z-dropdown)       /* 1000 */
var(--z-sticky)         /* 1020 */
var(--z-fixed)          /* 1030 */
var(--z-modal-backdrop) /* 1040 */
var(--z-modal)          /* 1050 */
```

---

**Copy & paste ready!** Just use `var(--variable-name)` in your CSS.
