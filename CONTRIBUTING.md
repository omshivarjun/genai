# Contributing to GenAI App Builder

First off, thank you for considering contributing to GenAI App Builder! It's people like you that make this tool amazing for everyone.

## 🚀 Quick Start

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Make your changes
4. Add tests if applicable
5. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
6. Push to the branch (`git push origin feature/AmazingFeature`)
7. Open a Pull Request

## 📋 Code of Conduct

This project and everyone participating in it is governed by our Code of Conduct. By participating, you are expected to uphold this code.

### Our Standards

- Use welcoming and inclusive language
- Be respectful of differing viewpoints and experiences
- Gracefully accept constructive criticism
- Focus on what is best for the community
- Show empathy towards other community members

## 🛠️ Development Setup

### Prerequisites

- Python 3.10 or higher
- Git
- Google Gemini API key for testing

### Installation

```bash
# Clone your fork
git clone https://github.com/YOUR_USERNAME/genai.git
cd genai

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install in development mode
pip install -e ".[dev]"

# Copy environment template
cp .env.example .env
# Add your API keys to .env
```

### Running Tests

```bash
# Run all tests
python -m pytest

# Run with coverage
python -m pytest --cov=agent

# Run specific test file
python -m pytest tests/test_agents.py
```

### Code Quality

We use several tools to maintain code quality:

```bash
# Format code
black agent/ tests/

# Check imports
isort agent/ tests/

# Lint code
flake8 agent/ tests/

# Type checking
mypy agent/
```

## 🎯 How to Contribute

### Reporting Bugs

Before creating bug reports, please check existing issues as you might find that you don't need to create one. When creating a bug report, please include as many details as possible:

- **Use a clear and descriptive title**
- **Describe the exact steps to reproduce the problem**
- **Provide specific examples to demonstrate the steps**
- **Describe the behavior you observed and what behavior you expected**
- **Include screenshots if applicable**
- **Include your environment details** (OS, Python version, etc.)

### Suggesting Enhancements

Enhancement suggestions are tracked as GitHub issues. When creating an enhancement suggestion:

- **Use a clear and descriptive title**
- **Provide a detailed description of the suggested enhancement**
- **Explain why this enhancement would be useful**
- **List any relevant examples from other tools**

### Pull Requests

1. **Follow the existing code style**
2. **Add tests for new functionality**
3. **Update documentation as needed**
4. **Ensure all tests pass**
5. **Write clear commit messages**
6. **Link to relevant issues**

## 📁 Project Structure

```
genai/
├── agent/                 # Core AI agents
│   ├── graph.py          # LangGraph workflow
│   ├── prompts.py        # AI prompts
│   ├── states.py         # State management
│   └── tools.py          # File operations
├── tests/                # Test suite
├── docs/                 # Documentation
├── examples/             # Usage examples
└── scripts/              # Utility scripts
```

## 🧪 Testing Guidelines

- Write tests for all new functionality
- Ensure tests are isolated and don't depend on external services
- Use meaningful test names that describe what is being tested
- Mock external API calls in tests
- Aim for high test coverage but focus on quality over quantity

### Test Categories

1. **Unit Tests**: Test individual functions and classes
2. **Integration Tests**: Test agent workflows and file generation
3. **End-to-End Tests**: Test complete project generation flows

## 📝 Documentation

- Update README.md for user-facing changes
- Add docstrings to new functions and classes
- Update CHANGELOG.md for all changes
- Include examples for new features

## 🎨 Coding Standards

### Python Style Guide

- Follow PEP 8
- Use type hints for function parameters and return values
- Keep functions focused and single-purpose
- Use meaningful variable and function names
- Add docstrings to public functions and classes

### Commit Message Format

```
<type>(<scope>): <subject>

<body>

<footer>
```

Types:
- `feat`: A new feature
- `fix`: A bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, missing semicolons, etc)
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Maintenance tasks

Example:
```
feat(coder): add support for React component generation

- Implement React component template system
- Add JSX syntax support in coder agent
- Update project structure for React apps

Closes #123
```

## 🚀 Release Process

1. Update version in `pyproject.toml`
2. Update `CHANGELOG.md` with new version
3. Create a release PR
4. After merge, tag the release
5. GitHub Actions will handle the rest

## ❓ Questions?

- Check existing [issues](https://github.com/omshivarjun/genai/issues)
- Start a [discussion](https://github.com/omshivarjun/genai/discussions)
- Contact maintainers directly

## 🏆 Recognition

Contributors will be recognized in:
- README.md contributors section
- Release notes for significant contributions
- Special mentions for outstanding contributions

Thank you for contributing! 🎉