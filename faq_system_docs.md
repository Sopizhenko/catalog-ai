# Pluggable FAQ System

A lightweight, pluggable FAQ system that can be easily integrated into any web project. The system provides categorized FAQs with real-time search functionality and keyword-based filtering.

## Features

- **Categorized FAQs**: Organize FAQs into logical categories
- **Real-time Search**: Search as you type across questions, answers, and keywords
- **Keyword Tagging**: Tag FAQs with relevant keywords for better discoverability
- **Responsive Design**: Works on desktop and mobile devices
- **Easy Integration**: Single HTML file with embedded CSS and JavaScript
- **JSON Data Structure**: Easily maintainable FAQ content in JSON format

## Data Structure

The FAQ system uses a JSON file (`faqs.json`) with the following structure:

```json
{
  "categories": [
    {
      "id": "general",
      "name": "General Questions",
      "description": "Common questions about our service"
    }
  ],
  "faqs": [
    {
      "id": "faq_1",
      "question": "How do I get started?",
      "answer": "To get started, simply create an account and follow the onboarding process.",
      "categoryId": "general",
      "keywords": ["getting started", "account", "onboarding", "setup"],
      "searchTerms": ["begin", "start", "new user", "registration"]
    }
  ]
}
```

### Data Fields Explained

#### Categories
- `id`: Unique identifier for the category
- `name`: Display name for the category
- `description`: Brief description of the category

#### FAQs
- `id`: Unique identifier for the FAQ
- `question`: The FAQ question
- `answer`: The answer (supports basic HTML)
- `categoryId`: References the category this FAQ belongs to
- `keywords`: Array of relevant keywords for filtering
- `searchTerms`: Additional search terms that don't appear in the question/answer

## Implementation Guide

### File Structure
```
project/
├── index.html          # Main FAQ system file
├── faqs.json          # FAQ data
└── README.md          # Documentation
```

### Integration Options

#### 1. Standalone Implementation
Use the provided HTML file as-is for a complete FAQ page.

#### 2. Widget Integration
Extract the JavaScript and CSS to embed the FAQ system within existing pages:

```html
<div id="faq-container"></div>
<script src="faq-system.js"></script>
```

#### 3. Framework Integration
The core JavaScript can be adapted for:
- React components
- Vue.js components  
- Angular components
- Web Components

## Customization

### Styling
The system uses CSS custom properties for easy theming:

```css
:root {
  --primary-color: #3b82f6;
  --secondary-color: #64748b;
  --background-color: #f8fafc;
  --text-color: #1e293b;
  --border-color: #e2e8f0;
}
```

### Search Configuration
Modify the search behavior by updating the search function:

```javascript
// Configure which fields to search
const searchFields = ['question', 'answer', 'keywords', 'searchTerms'];

// Configure search sensitivity
const searchOptions = {
  caseSensitive: false,
  includePartialMatches: true
};
```

## API Reference

### Core Functions

#### `loadFAQs(jsonPath)`
Loads FAQ data from JSON file.

#### `renderFAQs(faqs, categories)`
Renders the FAQ interface with provided data.

#### `searchFAQs(query)`
Performs real-time search across FAQ content.

#### `filterByCategory(categoryId)`
Filters FAQs by selected category.

### Events

#### FAQ Item Click
```javascript
document.addEventListener('faq-item-click', (event) => {
  console.log('FAQ clicked:', event.detail.faq);
});
```

#### Search Event
```javascript
document.addEventListener('faq-search', (event) => {
  console.log('Search query:', event.detail.query);
  console.log('Results count:', event.detail.count);
});
```

## Browser Support

- Chrome 60+
- Firefox 55+
- Safari 12+
- Edge 79+

## Performance Considerations

- **Lazy Loading**: Consider implementing lazy loading for large FAQ datasets
- **Debounced Search**: Search is debounced to prevent excessive filtering
- **Virtual Scrolling**: For 1000+ FAQs, implement virtual scrolling
- **Caching**: FAQ data is cached in memory after first load

## Accessibility Features

- **Keyboard Navigation**: Full keyboard support with Tab/Enter/Space
- **ARIA Labels**: Proper ARIA attributes for screen readers
- **Focus Management**: Logical focus order and visible focus indicators
- **Semantic HTML**: Proper heading hierarchy and semantic elements

## Usage Examples

### Basic Usage
```html
<!DOCTYPE html>
<html>
<head>
  <title>FAQ System</title>
</head>
<body>
  <div id="faq-system"></div>
  <script>
    // System auto-initializes and loads faqs.json
  </script>
</body>
</html>
```

### Custom Data Source
```javascript
// Load from custom API
fetch('/api/faqs')
  .then(response => response.json())
  .then(data => {
    renderFAQs(data.faqs, data.categories);
  });
```

### Programmatic Search
```javascript
// Trigger search programmatically
searchFAQs('payment methods');

// Clear search
searchFAQs('');
```

## Deployment

### Static Hosting
- Upload `index.html` and `faqs.json` to any web server
- No server-side requirements

### CDN Integration
- Host JSON file on CDN for better performance
- Update JSON path in configuration

### CMS Integration
- Connect to headless CMS for dynamic FAQ management
- Implement admin interface for FAQ editing

## Troubleshooting

### Common Issues

1. **FAQs not loading**: Check JSON file path and format
2. **Search not working**: Verify JavaScript console for errors
3. **Styling issues**: Check CSS custom properties and browser support
4. **Mobile responsiveness**: Test viewport meta tag is present

### Debug Mode
Enable debug mode for development:

```javascript
window.FAQDebug = true;
```

## Contributing

To extend the FAQ system:

1. Fork the repository
2. Create feature branch
3. Add tests for new functionality
4. Submit pull request

## License

MIT License - feel free to use in commercial and personal projects.

## Version History

- **v1.0.0**: Initial release with basic FAQ functionality
- **v1.1.0**: Added category filtering and improved search
- **v1.2.0**: Enhanced accessibility and mobile responsiveness