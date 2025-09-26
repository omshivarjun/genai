# Changelog

All notable changes to the GenAI App Builder project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2025-09-26

### Added
- Initial release of GenAI App Builder
- Google Gemini 2.0 Flash API integration
- Multi-agent architecture using LangGraph (Planner, Architect, Coder)
- Unique project folder generation system
- Support for generating HTML, CSS, and JavaScript web applications
- Environment variable management with `.env` support
- Comprehensive README with architecture diagrams
- MIT License
- Generated project examples:
  - Weather Dashboard with geolocation and API integration
  - To-Do List application with task management
  - Calculator with keyboard support and error handling

### Technical Details
- Python 3.10+ compatibility
- LangChain and LangGraph integration
- Pydantic for data validation
- UV package management support
- Cross-platform path handling
- Git integration with proper .gitignore

### Dependencies
- `google-generativeai>=0.8.3`
- `langchain-google-genai>=2.0.5`
- `langchain>=0.1.0`
- `langgraph>=0.1.0`
- `pydantic>=2.0.0`
- `python-dotenv>=1.0.0`

## [Unreleased]

### Planned Features
- Support for more project types (React, Vue, Node.js)
- Template system for custom project scaffolding
- API integration helpers and templates
- Dark/light theme support for generated projects
- Project preview and live reload capabilities
- Export to various deployment platforms
- Project customization options
- Batch project generation
- Plugin system for extending functionality

---

For more detailed information about changes, see the [commit history](https://github.com/omshivarjun/genai/commits/main).