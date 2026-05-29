# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**Mandala-Explorer** is an interactive web application for exploring the *Treasury of Precious Qualities* (Yonten Dzo), a Buddhist philosophical text. The application presents the text as a clickable mandala visualization with an accompanying outline/chapter navigator and detailed reading panel for individual verses.

- **Tech Stack**: Vue.js (3.x) single-page application
- **Deployment**: Single bundled HTML file (`index.html`)
- **UI Modes**: Dark mode (default) and light mode toggle
- **Text Source**: 13 chapters with full verse mappings

## Architecture & Structure

### Bundling System

The application uses a custom bundler that embeds all source code, styles, fonts, and data into a single `index.html` file. The bundler works by:

1. **Manifest** (`<script type="__bundler/manifest">`): JSON object mapping UUIDs to asset metadata (MIME type, compression, base64 data)
2. **Template** (`<script type="__bundler/template">`): The HTML template with UUID placeholders for assets
3. **Runtime unpacking**: JavaScript code in `<head>` decompresses assets (gzip) and creates blob URLs dynamically

**Editing approach**: Direct edits to the bundled HTML require identifying the correct section within the manifest/template. The bundler structure preserves all source code inline, making it inspectable but complex.

### Application Structure (Runtime)

The Vue.js app is initialized in the template and consists of:

- **Mandala Component**: Radial visualization with nested circles representing the text hierarchy (chapters → subsections → verses)
- **Outline Panel**: Left sidebar tree view for chapter/verse navigation
- **Reading Panel**: Right sidebar displaying selected verse text with attribution
- **Breadcrumb Navigation**: Shows current position and allows quick navigation up the hierarchy
- **Dark/Light Mode Toggle**: UI mode switcher affecting color scheme and typography

### Data Organization

- **Chapters**: 13 chapters covering different topics of the Treasury
- **Verses**: Individual text units mapped to mandala ring positions
- **Metadata**: Chapter names, verse ranges, section hierarchies embedded in the bundled data

## Common Development Tasks

### Viewing Changes

1. Open `index.html` directly in a browser (file:// works fine)
2. Changes to the HTML file update immediately on refresh

### Making Edits

The bundled structure means editing is tricky. Most changes fall into these categories:

**Text content updates** (verses, chapter titles, etc.):
- Located in the template section as JSON data structures
- Search for the text you want to change
- Make the edit and test in browser

**UI/styling changes** (colors, fonts, layout):
- CSS is embedded in `<style>` tags in the template
- Search for relevant class names or selectors
- Changes apply immediately on refresh

**Feature changes** (clicking behavior, panels, etc.):
- Vue component logic is embedded in the template
- Changes to event handlers or component methods require finding the Vue code section
- The code is minified/bundled, so use browser DevTools for inspection

### Testing

No formal test suite exists. Verification is manual:

1. Open `index.html` in browser
2. Test the specific feature (navigate mandala, open reading panel, toggle modes, etc.)
3. Verify no console errors appear (check DevTools)
4. Test both dark and light modes
5. Check breadcrumb navigation, verse transitions, and outline panel interactions

## Key Conventions

### Git Workflow

- Commits modify only `index.html` (containing bundled code and data)
- Commit messages use conventional format: `feat:`, `fix:`, `chore:`
- Each commit is a self-contained, deployed change

### Naming & Organization

- **Data IDs**: Verses and chapters use internal identifiers (UUIDs in the bundler, numeric IDs in Vue data)
- **CSS Classes**: Scoped to mode (`[data-mode="mandala"]`, `[data-mode="scriptorium"]`)
- **Component Names**: Follow Vue conventions (PascalCase for components)

### Domain Terminology

- **Mandala**: The radial visualization (circles, rings, clickable nodes)
- **Chapter**: Major topic grouping (13 total)
- **Verse**: Individual text unit (verse number varies by chapter)
- **Outline**: Tree-view navigation panel (left side)
- **Reading Panel**: Detail view for selected verse (right side)
- **Scriptorium Mode**: Alternative UI mode (warm parchment aesthetic, historical)
- **Treasury**: The full text being explored (Yonten Dzo)

## Development Notes

### Bundle Structure Visibility

You can inspect the bundled structure in browser DevTools:
1. Open `index.html` in browser
2. Open DevTools → Sources tab
3. Check `index.html` script content to see Vue code, styles, and data

### Performance Considerations

- The single-file bundle is ~5.4MB due to embedded fonts and data
- Gzip compression is applied to assets during bundling
- Browser decompresses on load (see `__bundler_thumbnail` for loading UI)

### Known Patterns

- **Verse Display**: Clicking mandala nodes or outline items updates the reading panel via Vue reactivity
- **Navigation State**: Current selection tracked in Vue `data`, reflected in breadcrumbs and visual highlighting
- **Mode Toggling**: CSS `[data-mode]` attribute controls styling; does not reload the page
- **Asset References**: Font files and other resources referenced by UUID are resolved at runtime via blob URLs

## Historical Context

Previous versions of this project included:
- `pack.py`: Bundler script (removed in commit 623a947)
- `extract_template.py`: Asset extraction tool (removed)
- Separate source files (now consolidated into single `index.html`)

The current workflow assumes the bundled HTML is the source of truth, with changes made directly to the template and data sections.
