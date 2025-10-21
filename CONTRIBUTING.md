# Contributing to PlantUML Generator

Thank you for your interest in contributing to the PlantUML Generator! This document provides guidelines and instructions for contributing.

## Table of Contents
- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [Making Changes](#making-changes)
- [Testing](#testing)
- [Submitting Changes](#submitting-changes)

## Code of Conduct

By participating in this project, you agree to maintain a respectful and inclusive environment for all contributors.

## Getting Started

1. Fork the repository
2. Clone your fork: `git clone https://github.com/your-username/puml-generator.git`
3. Create a feature branch: `git checkout -b feature/your-feature-name`

## Development Setup

### Prerequisites

- Docker (for containerized development)
- Python 3.11+ (for local development)
- Java 21+ (for running PlantUML locally)

### Local Development Without Docker

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Download PlantUML:
```bash
wget https://github.com/plantuml/plantuml/releases/download/v1.2024.7/plantuml-1.2024.7.jar
export PLANTUML_JAR=$(pwd)/plantuml-1.2024.7.jar
```

3. Run the processor:
```bash
python3 puml_processor.py examples/ -o output/
```

4. Run the server:
```bash
export SERVE_DIR=output
python3 server.py
```

### Docker Development

Build and test with Docker:
```bash
docker build -t puml-generator:dev .
docker run -v $(pwd)/examples:/input -v $(pwd)/output:/output puml-generator:dev process
```

## Making Changes

### Code Style

- Follow PEP 8 for Python code
- Use meaningful variable and function names
- Add docstrings to functions and classes
- Keep functions focused and modular

### Adding New Features

1. Create a new branch for your feature
2. Implement your changes
3. Add tests for new functionality
4. Update documentation (README.md, USAGE.md)
5. Test thoroughly

### Areas for Contribution

We welcome contributions in these areas:

- **Additional Output Formats**: Support for PDF, SVG, HTML, etc.
- **Enhanced Markdown**: Better styling, themes, custom templates
- **More CI/CD Integrations**: GitLab, Bitbucket, etc.
- **Performance Improvements**: Parallel processing, caching
- **Error Handling**: Better error messages and recovery
- **Configuration**: Support for config files (YAML, JSON)
- **Testing**: More comprehensive test coverage
- **Documentation**: Examples, tutorials, guides

## Testing

### Running Tests

Run the test suite:
```bash
./test.sh
```

### Manual Testing

1. Process example files:
```bash
docker run --rm \
  -v $(pwd)/examples:/input \
  -v $(pwd)/output:/output \
  puml-generator:test process
```

2. Verify output:
```bash
ls -R output/
cat output/index.md
```

3. Test web server:
```bash
docker run -d \
  -v $(pwd)/output:/output \
  -p 8080:8080 \
  --name test-server \
  puml-generator:test python3 /app/server.py

curl http://localhost:8080/index.md
docker stop test-server && docker rm test-server
```

### Adding Tests

When adding new functionality:

1. Add test cases to `test.sh`
2. Include example PlantUML files if needed
3. Verify all existing tests still pass

## Submitting Changes

### Pull Request Process

1. Ensure all tests pass
2. Update documentation to reflect changes
3. Add your changes to CHANGELOG.md (if exists)
4. Commit with clear, descriptive messages:
   ```
   Add feature: Support for SVG output format
   
   - Added SVG generation option to puml_processor.py
   - Updated Dockerfile to include SVG dependencies
   - Added tests for SVG output
   - Updated README with SVG usage examples
   ```

5. Push to your fork:
   ```bash
   git push origin feature/your-feature-name
   ```

6. Create a Pull Request with:
   - Clear title describing the change
   - Detailed description of what changed and why
   - Reference any related issues
   - Screenshots if UI changes are involved

### Commit Message Guidelines

- Use present tense ("Add feature" not "Added feature")
- Use imperative mood ("Move cursor to..." not "Moves cursor to...")
- First line should be 50 characters or less
- Reference issues and pull requests when relevant

### Review Process

1. Maintainers will review your PR
2. Address any feedback or requested changes
3. Once approved, your PR will be merged

## Project Structure

```
puml-generator/
├── Dockerfile              # Docker image definition
├── docker-compose.yml      # Docker Compose configuration
├── entrypoint.sh          # Container entrypoint script
├── puml_processor.py      # Main processing logic
├── server.py              # Web server
├── azure_wiki_publisher.py # Azure DevOps integration
├── requirements.txt       # Python dependencies
├── test.sh               # Test suite
├── examples/             # Example PlantUML files
│   ├── architecture/
│   └── sequences/
└── README.md             # Main documentation
```

## Development Tips

### Debugging

1. Run with verbose logging:
```bash
docker run --rm \
  -v $(pwd)/examples:/input \
  -v $(pwd)/output:/output \
  puml-generator:test \
  bash -c "python3 -u /app/puml_processor.py /input -o /output"
```

2. Access container shell:
```bash
docker run -it --rm \
  -v $(pwd)/examples:/input \
  puml-generator:test bash
```

### Performance Testing

Test with large numbers of files:
```bash
# Create test files
for i in {1..100}; do
  cat > examples/test-$i.puml << EOF
@startuml
actor User$i
User$i -> System : Request
@enduml
EOF
done

# Process and time
time docker run --rm \
  -v $(pwd)/examples:/input \
  -v $(pwd)/output:/output \
  puml-generator:test process
```

## Getting Help

- Open an issue for bugs or feature requests
- Check existing issues before creating new ones
- Provide detailed information about your environment
- Include error messages and logs

## License

By contributing, you agree that your contributions will be licensed under the same license as the project (MIT License).

## Recognition

Contributors will be recognized in the project documentation. Thank you for helping improve PlantUML Generator!
