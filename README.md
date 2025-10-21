# PlantUML Documentation Generator

A Docker-based solution for automatically generating diagrams and documentation from PlantUML files.

## Features

1. **Recursive PlantUML Processing**: Automatically finds and processes PlantUML files in nested directories
2. **Diagram Generation**: Converts PlantUML files to PNG diagrams
3. **Markdown Documentation**: Creates markdown files with embedded diagrams
4. **Web Server**: Serves generated documentation via HTTP
5. **Azure DevOps Integration**: Optionally publish documentation to Azure DevOps wiki
6. **Docker-based**: Easy deployment and consistent environment

## Quick Start

### Building the Docker Image

```bash
docker build -t puml-generator .
```

### Basic Usage - Process and Serve

Process PlantUML files and serve the documentation:

```bash
docker run -d \
  -v /path/to/your/plantuml/files:/input \
  -v /path/to/output:/output \
  -p 8080:8080 \
  puml-generator serve
```

Then open your browser to `http://localhost:8080` to view the documentation.

### Process Only

To just process files without starting the web server:

```bash
docker run \
  -v /path/to/your/plantuml/files:/input \
  -v /path/to/output:/output \
  puml-generator process
```

### Publish to Azure DevOps Wiki

```bash
docker run \
  -v /path/to/your/plantuml/files:/input \
  -e AZURE_DEVOPS_ORG=your-organization \
  -e AZURE_DEVOPS_PROJECT=your-project \
  -e AZURE_DEVOPS_WIKI_ID=your-wiki-id \
  -e AZURE_DEVOPS_PAT=your-personal-access-token \
  -e AZURE_DEVOPS_WIKI_PATH=/PlantUML \
  puml-generator publish
```

### Process, Publish, and Serve

```bash
docker run -d \
  -v /path/to/your/plantuml/files:/input \
  -v /path/to/output:/output \
  -p 8080:8080 \
  -e AZURE_DEVOPS_ORG=your-organization \
  -e AZURE_DEVOPS_PROJECT=your-project \
  -e AZURE_DEVOPS_WIKI_ID=your-wiki-id \
  -e AZURE_DEVOPS_PAT=your-personal-access-token \
  puml-generator process-and-publish
```

## Directory Structure

### Input Directory

Your PlantUML files can be organized in any directory structure:

```
input/
├── architecture/
│   ├── system-design.puml
│   └── component-diagram.puml
├── sequences/
│   ├── login-flow.puml
│   └── api-calls.puml
└── other-diagrams.puml
```

### Output Directory

Generated files maintain the same directory structure:

```
output/
├── index.md                    # Main index with links to all diagrams
├── architecture/
│   ├── system-design.png
│   ├── system-design.md
│   ├── component-diagram.png
│   └── component-diagram.md
└── sequences/
    ├── login-flow.png
    ├── login-flow.md
    ├── api-calls.png
    └── api-calls.md
```

## Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `INPUT_DIR` | Directory containing PlantUML files | `/input` |
| `OUTPUT_DIR` | Directory for generated files | `/output` |
| `PORT` | Port for web server | `8080` |
| `PLANTUML_JAR` | Path to PlantUML JAR file | `/opt/plantuml.jar` |
| `AZURE_DEVOPS_ORG` | Azure DevOps organization | - |
| `AZURE_DEVOPS_PROJECT` | Azure DevOps project | - |
| `AZURE_DEVOPS_WIKI_ID` | Wiki identifier | - |
| `AZURE_DEVOPS_PAT` | Personal Access Token | - |
| `AZURE_DEVOPS_WIKI_PATH` | Base path in wiki | `/PlantUML` |

### Supported File Extensions

The generator looks for files with the following extensions:
- `.puml`
- `.plantuml`
- `.pu`

## Commands

The Docker container supports the following commands:

- `serve` (default): Process files and start web server
- `process`: Only process files, don't start server
- `publish`: Process files and publish to Azure DevOps wiki
- `process-and-publish`: Process, publish to wiki, then serve

## Examples

Example PlantUML files are provided in the `examples/` directory:

```bash
# Try with examples
docker run -d \
  -v $(pwd)/examples:/input \
  -v $(pwd)/output:/output \
  -p 8080:8080 \
  puml-generator serve
```

## Azure DevOps Setup

To publish to Azure DevOps wiki:

1. Create a Personal Access Token (PAT) with Wiki permissions
2. Find your wiki ID from Azure DevOps wiki URL
3. Set the required environment variables when running the container

## Development

### Running Scripts Directly

```bash
# Process PlantUML files
python3 puml_processor.py /path/to/input -o /path/to/output

# Start web server
python3 server.py

# Publish to Azure DevOps
python3 azure_wiki_publisher.py /path/to/output \
  --organization your-org \
  --project your-project \
  --wiki-id your-wiki-id \
  --pat-token your-token
```

### Requirements

- Python 3.11+
- Java 17+ (for PlantUML)
- GraphViz (for diagram rendering)
- PlantUML JAR file

## License

MIT License

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.