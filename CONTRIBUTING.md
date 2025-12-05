# Contributing to Emotion Music Generator

Thank you for your interest in contributing! This document provides guidelines and instructions for contributing.

## Code of Conduct

Be respectful, inclusive, and professional in all interactions.

## How to Contribute

### Reporting Bugs

1. Check if the bug already exists in Issues
2. Use a descriptive title
3. Provide detailed description with steps to reproduce
4. Include environment details (OS, Python version, etc.)
5. Attach screenshots if applicable

### Suggesting Features

1. Check if feature exists in Issues
2. Provide clear use case and benefits
3. Include code examples if relevant

### Pull Requests

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature`
3. Make your changes with clear commit messages
4. Follow PEP 8 style guidelines
5. Test your changes
6. Push to your fork
7. Submit a pull request with detailed description

## Development Setup

```bash
# Clone your fork
git clone https://github.com/yourusername/emotion-music-generator.git
cd emotion-music-generator2

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install development tools (optional)
pip install pytest black flake8 mypy
```

## Code Style

- Follow PEP 8
- Use meaningful variable names
- Add docstrings to functions
- Keep lines under 100 characters
- Use type hints where applicable

## Testing

```bash
# Run tests
pytest

# Check code style
flake8 src/

# Format code
black src/
```

## Commit Message Format

```
<type>: <subject>

<body>

<footer>
```

Types: feat, fix, docs, style, refactor, test, chore

## License

By contributing, you agree your code is licensed under MIT License.
