# Implementation Tasks

## 1. Widget Replacement
- [ ] 1.1 Replace Label with Textual's Static widget with word-wrap enabled
- [ ] 1.2 Use VerticalScroll container for article content
- [ ] 1.3 Configure CSS to enable word-wrap and disable horizontal scroll
- [ ] 1.4 Test that text wraps at panel boundaries

## 2. Content Formatting
- [ ] 2.1 Ensure title remains bold and readable
- [ ] 2.2 Preserve metadata formatting (date, link, liked status)
- [ ] 2.3 Handle long URLs with proper wrapping or truncation
- [ ] 2.4 Maintain paragraph breaks and whitespace

## 3. Scrolling Behavior
- [ ] 3.1 Verify vertical scrolling works for long articles
- [ ] 3.2 Ensure no horizontal scrollbar appears
- [ ] 3.3 Test with vim-style scrolling (ctrl+u/ctrl+d)
- [ ] 3.4 Test with page up/page down keys

## 4. Testing & Validation
- [ ] 4.1 Test with short articles (< panel width)
- [ ] 4.2 Test with long paragraphs (> panel width)
- [ ] 4.3 Test with articles containing long URLs
- [ ] 4.4 Test on different terminal widths (80, 120, 160 columns)
- [ ] 4.5 Verify no text is cut off or hidden

## 5. Documentation
- [ ] 5.1 Update design doc if needed
- [ ] 5.2 No README changes needed (internal improvement)
