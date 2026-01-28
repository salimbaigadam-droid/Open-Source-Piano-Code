# Contributing to Chromatic Cascade

Thank you for your interest in contributing! This project welcomes contributions from developers of all skill levels.

## 🌟 Ways to Contribute

- 🐛 **Report Bugs** - Open an issue describing the problem
- 💡 **Suggest Features** - Share ideas for improvements
- 📝 **Improve Documentation** - Fix typos, add examples, clarify instructions
- 🎨 **Enhance UI/UX** - Improve the design or user experience
- 🔧 **Fix Issues** - Submit pull requests for open issues
- 🎵 **Add Features** - Implement new audio effects, instruments, or backends

## 🚀 Getting Started

1. **Fork the repository**
2. **Clone your fork**
   ```bash
   git clone https://github.com/YOUR-USERNAME/chromatic-cascade.git
   cd chromatic-cascade
   ```
3. **Create a branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```
4. **Make your changes**
5. **Test your changes** - Ensure everything works
6. **Commit your changes**
   ```bash
   git commit -m "Add: brief description of changes"
   ```
7. **Push to your fork**
   ```bash
   git push origin feature/your-feature-name
   ```
8. **Open a Pull Request**

## 📋 Pull Request Guidelines

### Before Submitting
- [ ] Code follows existing style conventions
- [ ] All tests pass (if applicable)
- [ ] Documentation updated (if needed)
- [ ] Commit messages are clear and descriptive

### PR Description Should Include
- **What**: Brief description of changes
- **Why**: Motivation or issue being addressed
- **How**: Technical approach or implementation details
- **Testing**: How you tested the changes

### Example PR Template
```markdown
## Description
Brief description of what this PR does

## Motivation
Why is this change needed? What problem does it solve?

## Changes
- List of specific changes made

## Testing
How was this tested?

## Screenshots (if UI changes)
Include before/after screenshots
```

## 🎨 Code Style Guidelines

### Frontend (JavaScript/React)
- Use functional components with hooks
- Keep components under 300 lines
- Use meaningful variable names
- Add comments for complex logic
- Follow existing naming conventions

### Python Backend
- Follow PEP 8 style guide
- Use type hints where applicable
- Document functions with docstrings
- Keep functions focused (single responsibility)
- Use meaningful class and function names

### Go Backend
- Follow standard Go formatting (`gofmt`)
- Use `golint` for linting
- Write clear comments for exported functions
- Keep functions under 50 lines when possible
- Use descriptive variable names

### Rust Backend
- Follow Rust naming conventions
- Run `cargo fmt` before committing
- Run `cargo clippy` and fix warnings
- Document public APIs
- Use meaningful type names

## 🧪 Testing

### Frontend Testing
```bash
# Open piano.html in browser
# Test each feature manually
# Check browser console for errors
```

### Backend Testing
```bash
# Python
cd backend-python
pytest  # if tests exist

# Go
cd backend-go
go test ./...

# Rust
cd backend-rust
cargo test
```

## 📁 Project Structure

When adding new features, maintain the existing structure:

```
piano-app/
├── frontend/           # All frontend code
├── backend-python/     # Python microservices
├── backend-go/         # Go pipeline
├── backend-rust/       # Rust actors
└── docs/              # Documentation (if adding)
```

## 🐛 Bug Reports

When reporting bugs, include:

1. **Description** - Clear description of the bug
2. **Steps to Reproduce**
   - Step 1
   - Step 2
   - Step 3
3. **Expected Behavior** - What should happen
4. **Actual Behavior** - What actually happens
5. **Environment**
   - OS: (e.g., macOS 13, Ubuntu 22.04)
   - Browser: (e.g., Chrome 120, Firefox 121)
   - Backend: (Python/Go/Rust version)
6. **Screenshots** - If applicable

## 💡 Feature Requests

When suggesting features, include:

1. **Problem** - What problem does this solve?
2. **Proposed Solution** - How should it work?
3. **Alternatives** - Other approaches you considered
4. **Additional Context** - Screenshots, mockups, examples

## 🏗️ Architecture Contributions

This project showcases three different architectures. When contributing:

### Adding to Existing Backends
- Maintain the architectural pattern (microservices/pipeline/actors)
- Keep consistency with existing code style
- Update documentation if adding new services/stages/actors

### Adding New Backends
If you want to add a new backend in a different language:
1. Choose a distinct architectural pattern (not already used)
2. Document the architecture thoroughly
3. Maintain feature parity with existing backends
4. Add to README comparison table

Good candidates:
- **Elixir** - Supervisor trees pattern
- **Erlang** - OTP behaviors pattern
- **Java** - Spring Boot microservices
- **Node.js** - Event-driven architecture
- **C++** - High-performance threading

## 🎵 Audio/MIDI Contributions

When working on audio features:
- Test with real MIDI devices if possible
- Ensure cross-browser compatibility
- Consider performance impact
- Document sample rates, bit depths, etc.

## 📖 Documentation Contributions

Documentation improvements are always welcome:
- Fix typos or grammatical errors
- Add examples or tutorials
- Improve clarity of explanations
- Add diagrams or visualizations
- Translate to other languages

## ❓ Questions?

- Open a [Discussion](https://github.com/YOUR-USERNAME/chromatic-cascade/discussions)
- Ask in an issue with the `question` label
- Check existing issues/discussions first

## 🙏 Code of Conduct

### Our Standards
- Be respectful and inclusive
- Welcome newcomers
- Accept constructive criticism gracefully
- Focus on what's best for the project
- Show empathy towards others

### Not Acceptable
- Harassment or discriminatory language
- Trolling or insulting comments
- Personal or political attacks
- Publishing others' private information

## 📜 License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

Thank you for contributing to Chromatic Cascade! 🎹✨
