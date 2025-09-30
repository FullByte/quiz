# Copilot Instructions - Quiz Center

## Project Overview

This is a **static web-based quiz platform** with Python management tools. The architecture uses a hub-and-spoke model where:
- **Root level**: Central hub (`index.html`) displaying all quiz categories
- **Category directories**: Organized folders like `sport/`, `gesetze/`, `ai/`, each containing multiple quiz instances
- **Quiz instances**: Self-contained folders with `quiz.json`, `index.html`, `script.js`, `styles.css`, and optional `banner.png`

## Core Architecture Patterns

### 1. Configuration-Driven System
- **Central config**: `config.json` defines all categories and quiz mappings
- **Auto-discovery**: `update_config.py` scans filesystem and syncs configuration
- **Schema validation**: `_template/schema.json` defines required quiz.json structure

### 2. Template-Based Creation
- **Template source**: `_template/copyme/` contains ready-to-use quiz template files
- **Standardized structure**: All quiz instances follow identical file patterns
- **Consistent styling**: FontAwesome icons, responsive design, bounce animations

### 3. Four-Step Quiz Creation Process
Follow this exact workflow documented in `_template/instruction.md`:

1. **Quiz Structure Setup**: Copy template files, choose URL-friendly names
2. **Generate quiz.json**: Create 100 questions from PDF sources using schema validation
3. **Create banner.png**: Design 1200x300px banners with thematic illustrations
4. **HTML/CSS Customization**: Update titles, favicons, and loading animations

```bash
# Step 1: Create structure
mkdir [category]/[quiz_name]
cp -r _template/copyme/* [category]/[quiz_name]/
python update_config.py

# Steps 2-4: Content creation (see detailed workflows below)
```

## File Structure Conventions

### Category Organization
```
[category]/[quiz-name]/     # e.g., sport/basketball/
├── quiz.json              # Quiz data (follows schema.json)
├── index.html             # Quiz UI (copy from template)
├── script.js              # Quiz logic (copy from template) 
├── styles.css             # Styling (copy from template)
├── fontawesome.css        # Icons (copy from template)
├── banner.png             # Optional 400x200px image
└── [source].pdf           # Optional reference document
```

### Configuration Structure
- **config.json**: Maps categories → quiz arrays, defines icons and descriptions
- **Default category icons**: Predefined in `update_config.py` (ai=fa-robot, sport=fa-football, etc.)
- **Excluded directories**: Anything starting with `_`, `.git`, `__pycache__`, `node_modules`

## Development Patterns

### Quiz.json Structure (Critical)
```json
{
  "quiz": {
    "title": "Quiz Name",
    "description": "Description with {questionCount} placeholder",
    "language": "de",
    "version": "1.0",
    "sourceDocument": { "title": "", "version": "", "year": 2024, "pdfFilename": "" },
    "settings": { "shuffleQuestions": true, "shuffleOptions": true, "showExplanations": true, "timePerQuestionSec": 60 },
    "questions": [
      {
        "id": "q1",
        "text": "Question text",
        "options": ["Option 1", "Option 2", "Option 3", "Option 4"],
        "correctIndex": 0,
        "explanation": "Why this answer is correct",
        "source": { "citation": "", "pages": "", "chapter": "" },
        "tags": ["tag1", "tag2"],
        "difficulty": "leicht|mittel|schwer"
      }
    ]
  }
}
```

### JavaScript Architecture
- **Hub script** (`script.js`): Loads config.json, renders category cards, handles navigation
- **Quiz scripts**: Self-contained quiz logic, question randomization, scoring, PDF viewing
- **Common patterns**: Fetch-based loading, screen management, progress tracking, responsive design

### CSS Framework
- **Responsive design**: Mobile-first approach with flexbox/grid
- **Glass-morphism**: Backdrop-filter effects throughout
- **Component classes**: `.category-card`, `.quiz-question`, `.feedback-container`
- **State management**: Screen visibility, loading states, animations

## Development Workflows

### Step 1: Quiz Structure Setup
**Naming Conventions (Critical)**:
- Format: URL-friendly, lowercase, short
- Use underscores for multi-word names: `machine_learning`, `data_science`
- ✅ Good: `basketball`, `tennis`, `grundgesetz`
- ❌ Bad: `Hobbyhorsing Quiz`, `LLM-Engineer`

**Category Assignment**:
- `ai/`: Artificial Intelligence, Programming, Tech
- `sport/`: All sports and physical activities  
- `gesetze/`: Legal sciences, laws, regulations, constitution
- Create new categories as needed

```bash
# Template setup example
mkdir sport/basketball
cp -r _template/copyme/* sport/basketball/
python update_config.py  # Updates config.json automatically
```

### Step 2: Generate quiz.json from PDF Sources
**Requirements for AI Quiz Generation**:
- Extract ~100 factual questions from provided PDF
- Follow `_template/schema.json` structure exactly
- Question types: Definitions, rules, thresholds, procedures, exceptions, deadlines
- Each question: 4 options (1 correct, 3 plausible distractors)
- Include difficulty tags: `leicht|mittel|schwer`
- Precise source citations with page numbers and chapters

**AI Workflow**:
1. Analyze PDF content for knowledge bits
2. Create questions with explanations
3. Validate against schema.json
4. Generate in batches (20-30 questions per iteration)
5. Offer JSON download due to length

### Step 3: Create Thematic Banner (1200x300px)
**Design Requirements**:
- Wide banner format (4:1 ratio)
- Modern, professional style matching app colors (#546de5)
- Thematic illustration without text overlay
- Creative typography if including category name
- Save as `banner.png` in quiz folder

### Step 4: HTML/CSS Customization
**Required Changes**:
```html
<!-- Update page title -->
<title>[CATEGORY_NAME] Quiz</title>

<!-- Update favicon with thematic emoji -->
<link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><text y='.9em' font-size='90'>⚽</text></svg>">

<!-- Update loading animation -->
<div class="loading-spinner">⚽</div>
<p>[CATEGORY_NAME] Quiz wird geladen...</p>
```

**Emoji Mappings**:
- Sport: ⚽🏀🎾🤾🐎 (football, basketball, tennis, handball, hobbyhorsing)
- Legal: ⚖️📜📋 (justice, constitution, civil law)
- AI: 🤖 (robot)

### Validation & Quality Control
**Schema Validation**:
```bash
# Validate quiz.json structure
npx ajv validate -s _template/schema.json -d [category]/[quiz]/quiz.json

# Update and validate config
python update_config.py
```

**File Structure Checklist**:
- [ ] All template files copied (`index.html`, `styles.css`, `script.js`, `fontawesome.css`)
- [ ] `quiz.json` follows schema with ~100 questions
- [ ] `banner.png` created (1200x300px recommended)
- [ ] HTML customized (title, favicon, loading animation)
- [ ] Config updated with `python update_config.py`

### Debugging Common Issues
- **Quiz not appearing**: Run `python update_config.py` to sync filesystem with config.json
- **Invalid quiz data**: Validate against `_template/schema.json` - check question structure
- **Missing dependencies**: Ensure ALL files copied from `_template/copyme/`
- **Console errors**: Check browser dev tools for fetch failures or malformed JSON
- **Excluded directories**: Script ignores folders starting with `_`, `.git`, `__pycache__`, `node_modules`

### Code Style Conventions
- **German UI text**: All user-facing text in German ("Quiz wird geladen...", etc.)
- **Semantic HTML**: Proper heading hierarchy, ARIA labels for accessibility
- **Progressive enhancement**: Core functionality works without JavaScript
- **FontAwesome icons**: Self-hosted, consistent usage across components
- **URL-friendly naming**: Lowercase, underscores for separators, no special characters

## Integration Points

### Python-Web Interface
- **Config generation**: Python scans filesystem → generates config.json → JavaScript loads it
- **No runtime coupling**: Python tools are build-time only, web app is fully static
- **Local development**: Use `python -m http.server 8000` or VS Code Live Server

### Asset Management
- **Banner images**: Optional, 400x200px, displayed in category cards and quiz headers
- **PDF documents**: Optional source materials, accessible via "PDF anzeigen" button
- **FontAwesome**: Self-hosted CSS file, no CDN dependencies

Remember: This is a **static website** - all interactivity is client-side JavaScript, no server-side processing required.