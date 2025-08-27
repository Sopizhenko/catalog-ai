# Catalog AI - Theming Quick Reference

> **Quick reference for developers working on Catalog AI**

## 🎨 Most Used Colors

```css
/* Primary (Confirma Green) */
--primary-brand: #009607     /* Main brand color */
--primary-100: #dcfce7       /* Light backgrounds */
--primary-600: #008005       /* Buttons, links */

/* Text Colors */
--secondary-800: #1e293b     /* Primary text */
--secondary-600: #475569     /* Secondary text */
--secondary-500: #64748b     /* Muted text */

/* Backgrounds */
--white: #ffffff             /* Cards, modals */
--secondary-50: #f8fafc      /* Page background */
--secondary-100: #f1f5f9     /* Subtle backgrounds */

/* Accents */
--accent-600: #2563eb        /* Blue accents */
--accent-100: #dbeafe        /* Light blue backgrounds */
```

## 📏 Common Spacing

```css
--space-2: 0.5rem    /* 8px  - Small gaps */
--space-4: 1rem      /* 16px - Standard padding */
--space-6: 1.5rem    /* 24px - Card padding */
--space-8: 2rem      /* 32px - Section spacing */
```

## 🔤 Typography Scale

```css
--text-xs: 0.75rem    /* 12px - Tags, badges */
--text-sm: 0.875rem   /* 14px - Labels, captions */
--text-base: 1rem     /* 16px - Body text */
--text-lg: 1.125rem   /* 18px - Subtitles */
--text-xl: 1.25rem    /* 20px - Card titles */
--text-2xl: 1.5rem    /* 24px - Section headings */
```

## ⚡ Quick Component Patterns

### Standard Card
```css
.my-card {
  background: var(--white);
  border: 1px solid var(--secondary-200);
  box-shadow: var(--shadow-lg);
  padding: var(--space-8);
  transition: var(--transition-normal);
}

.my-card:hover {
  transform: translateY(-4px);
  box-shadow: var(--shadow-2xl);
}
```

### Primary Button
```css
.my-button {
  background: var(--primary-brand);
  color: var(--white);
  padding: var(--space-4) var(--space-6);
  border: none;
  border-radius: var(--radius-full);
  font-weight: var(--font-semibold);
  transition: var(--transition-normal);
}

.my-button:hover {
  background: var(--primary-700);
  transform: translateY(-2px);
}
```

### Tag/Badge
```css
.my-tag {
  background: var(--primary-100);
  color: var(--primary-700);
  padding: var(--space-1) var(--space-3);
  border-radius: var(--radius-full);
  font-size: var(--text-xs);
  font-weight: var(--font-semibold);
}
```

### Input Field
```css
.my-input {
  padding: var(--space-4);
  border: 2px solid var(--secondary-300);
  background: var(--white);
  font-size: var(--text-base);
  transition: var(--transition-normal);
}

.my-input:focus {
  border-color: var(--primary-500);
  outline: 2px solid var(--primary-500);
  outline-offset: 2px;
}
```

## 🎭 Animation Classes

```css
/* Fade in elements */
.animate-fade-in

/* Card entrance animation */
.animate-card-enter

/* Slide up animation */  
.animate-slide-up

/* For elements that should exit */
.animate-card-exit
.animate-slide-down
```

## 📱 Responsive Breakpoints

```css
/* Tablet (2 columns) */
@media (max-width: 1024px) { }

/* Mobile (1 column) */
@media (max-width: 768px) { }

/* Small mobile (compact) */
@media (max-width: 480px) { }
```

## 🚨 Common Mistakes to Avoid

❌ **Don't use hardcoded colors**
```css
color: #009607; /* Wrong */
```

✅ **Use CSS variables**
```css
color: var(--primary-brand); /* Correct */
```

❌ **Don't use hardcoded spacing**
```css
padding: 16px; /* Wrong */
```

✅ **Use spacing tokens**
```css
padding: var(--space-4); /* Correct */
```

❌ **Don't animate layout properties**
```css
transition: width 0.3s; /* Causes layout thrashing */
```

✅ **Animate transform/opacity**
```css
transition: transform 0.3s; /* GPU accelerated */
```

## 🔧 Development Checklist

When creating new components:

- [ ] Use CSS custom properties for colors
- [ ] Use spacing tokens for padding/margin
- [ ] Include hover/focus states
- [ ] Test on mobile breakpoints
- [ ] Verify contrast ratios (min 4.5:1)
- [ ] Add appropriate transitions
- [ ] Use semantic HTML elements
- [ ] Include ARIA attributes if needed

## 💡 Pro Tips

1. **Consistent Hover Effects**: Use `translateY(-4px)` for cards, `translateY(-2px)` for buttons

2. **Layer Order**: Cards use `--shadow-lg`, modals use `--shadow-2xl`

3. **Border Radius**: Confirma brand uses sharp edges (`border-radius: 0`), except for pills/badges (`border-radius: var(--radius-full)`)

4. **Color Hierarchy**: 
   - 900-800: Dark text
   - 600-700: Medium text, buttons
   - 300-400: Borders, dividers  
   - 50-100: Light backgrounds

5. **Font Weights**:
   - 400: Body text
   - 500: Labels
   - 600: Headings
   - 700: Emphasis

---

**Need more details?** → See `THEMING_GUIDE.md` for complete documentation
