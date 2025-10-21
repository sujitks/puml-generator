# PlantUML Generator - Usage Guide

This guide provides detailed instructions on how to use the PlantUML Documentation Generator.

## Table of Contents
- [Quick Start](#quick-start)
- [Basic Usage](#basic-usage)
- [Advanced Usage](#advanced-usage)
- [Azure DevOps Integration](#azure-devops-integration)
- [Customization](#customization)
- [Troubleshooting](#troubleshooting)

## Quick Start

### 1. Build the Docker Image

```bash
docker build -t puml-generator .
```

Or use Docker Compose:

```bash
docker-compose build
```

### 2. Run with Example Files

```bash
# Using Docker
docker run -d \
  -v $(pwd)/examples:/input \
  -v $(pwd)/output:/output \
  -p 8080:8080 \
  puml-generator

# Using Docker Compose
docker-compose up -d
```

### 3. View Documentation

Open your browser to http://localhost:8080 to view the generated documentation.

## Basic Usage

### Process PlantUML Files Only

If you only want to generate diagrams and markdown files without starting the web server:

```bash
docker run --rm \
  -v /path/to/your/plantuml/files:/input \
  -v /path/to/output:/output \
  puml-generator process
```

This will:
- Find all `.puml`, `.plantuml`, and `.pu` files in `/input`
- Generate PNG diagrams for each file
- Create markdown documentation with embedded diagrams
- Create an index file listing all diagrams

### Process and Serve

To both process files and start the web server:

```bash
docker run -d \
  -v /path/to/your/plantuml/files:/input \
  -v /path/to/output:/output \
  -p 8080:8080 \
  puml-generator serve
```

This is the default behavior and will:
- Process all PlantUML files
- Start a web server on port 8080
- Serve the generated documentation

## Advanced Usage

### Custom Port

To use a different port for the web server:

```bash
docker run -d \
  -v /path/to/your/plantuml/files:/input \
  -v /path/to/output:/output \
  -p 3000:3000 \
  -e PORT=3000 \
  puml-generator serve
```

### Using Different Directories

You can specify custom input and output directories:

```bash
docker run -d \
  -v /path/to/your/plantuml/files:/custom-input \
  -v /path/to/output:/custom-output \
  -e INPUT_DIR=/custom-input \
  -e OUTPUT_DIR=/custom-output \
  -p 8080:8080 \
  puml-generator serve
```

### Running Scripts Directly

You can also run the Python scripts directly without using the entrypoint:

```bash
# Process only
docker run --rm \
  -v $(pwd)/examples:/input \
  -v $(pwd)/output:/output \
  puml-generator python3 /app/puml_processor.py /input -o /output

# Start server only (files must already be processed)
docker run -d \
  -v $(pwd)/output:/output \
  -p 8080:8080 \
  -e SERVE_DIR=/output \
  puml-generator python3 /app/server.py
```

## Azure DevOps Integration

### Prerequisites

1. An Azure DevOps organization and project
2. A wiki in your project
3. A Personal Access Token (PAT) with wiki permissions

### Finding Your Wiki ID

You can find your wiki ID in the Azure DevOps wiki URL:
```
https://dev.azure.com/{organization}/{project}/_wiki/wikis/{wiki-id}
```

### Publishing to Azure DevOps

```bash
docker run --rm \
  -v /path/to/your/plantuml/files:/input \
  -e AZURE_DEVOPS_ORG=your-organization \
  -e AZURE_DEVOPS_PROJECT=your-project \
  -e AZURE_DEVOPS_WIKI_ID=your-wiki-id \
  -e AZURE_DEVOPS_PAT=your-personal-access-token \
  -e AZURE_DEVOPS_WIKI_PATH=/PlantUML \
  puml-generator publish
```

### Publishing and Serving

To publish to Azure DevOps and then serve locally:

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

### Storing PAT Securely

Instead of passing the PAT directly, you can use a file:

```bash
# Save PAT to a file
echo "your-pat-token" > azure-pat.txt

# Use it with Docker
docker run --rm \
  -v /path/to/your/plantuml/files:/input \
  -v $(pwd)/azure-pat.txt:/secrets/pat.txt \
  -e AZURE_DEVOPS_ORG=your-organization \
  -e AZURE_DEVOPS_PROJECT=your-project \
  -e AZURE_DEVOPS_WIKI_ID=your-wiki-id \
  -e AZURE_DEVOPS_PAT=$(cat /secrets/pat.txt) \
  puml-generator publish
```

## Customization

### File Structure

The generator maintains your directory structure:

**Input:**
```
plantuml-files/
├── architecture/
│   ├── system.puml
│   └── components.puml
├── sequences/
│   └── user-flow.puml
└── diagrams.puml
```

**Output:**
```
output/
├── index.md                    # Generated index
├── architecture/
│   ├── system.png
│   ├── system.md
│   ├── components.png
│   └── components.md
├── sequences/
│   ├── user-flow.png
│   └── user-flow.md
├── diagrams.png
└── diagrams.md
```

### Supported File Extensions

The generator recognizes these PlantUML file extensions:
- `.puml`
- `.plantuml`
- `.pu`

### Environment Variables Reference

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `INPUT_DIR` | Directory containing PlantUML files | `/input` | No |
| `OUTPUT_DIR` | Directory for generated files | `/output` | No |
| `PORT` | Port for web server | `8080` | No |
| `PLANTUML_JAR` | Path to PlantUML JAR file | `/opt/plantuml.jar` | No |
| `AZURE_DEVOPS_ORG` | Azure DevOps organization | - | For publishing |
| `AZURE_DEVOPS_PROJECT` | Azure DevOps project | - | For publishing |
| `AZURE_DEVOPS_WIKI_ID` | Wiki identifier | - | For publishing |
| `AZURE_DEVOPS_PAT` | Personal Access Token | - | For publishing |
| `AZURE_DEVOPS_WIKI_PATH` | Base path in wiki | `/PlantUML` | No |

## Troubleshooting

### Issue: No files processed

**Cause:** PlantUML files might have unsupported extensions or are in the wrong directory.

**Solution:** 
- Ensure files have `.puml`, `.plantuml`, or `.pu` extensions
- Check that the input volume is mounted correctly
- Verify files are not in hidden directories

### Issue: Diagrams not generating

**Cause:** PlantUML syntax errors or Java issues.

**Solution:**
- Check PlantUML syntax in your files
- View container logs: `docker logs <container-name>`
- Test PlantUML locally to verify syntax

### Issue: Web server not accessible

**Cause:** Port mapping or firewall issues.

**Solution:**
- Ensure port is correctly mapped: `-p 8080:8080`
- Check if port is already in use
- Verify firewall allows connections on the port

### Issue: Azure DevOps publishing fails

**Cause:** Invalid credentials or permissions.

**Solution:**
- Verify PAT token has wiki permissions
- Check organization, project, and wiki ID are correct
- Ensure network can reach Azure DevOps

### Viewing Container Logs

```bash
# For running containers
docker logs <container-name>

# Follow logs in real-time
docker logs -f <container-name>

# For docker-compose
docker-compose logs
```

### Testing PlantUML Syntax

To test if a PlantUML file is valid before processing:

```bash
docker run --rm \
  -v $(pwd)/my-file.puml:/test.puml \
  puml-generator \
  java -jar /opt/plantuml.jar -syntax /test.puml
```

## Examples

### Example 1: Process Local Files

```bash
# Create a directory with PlantUML files
mkdir -p my-diagrams/architecture
cat > my-diagrams/architecture/system.puml << 'EOF'
@startuml
actor User
User -> System : Request
System -> Database : Query
Database -> System : Data
System -> User : Response
@enduml
EOF

# Process and serve
docker run -d \
  -v $(pwd)/my-diagrams:/input \
  -v $(pwd)/docs:/output \
  -p 8080:8080 \
  --name my-puml-server \
  puml-generator serve

# View in browser: http://localhost:8080
```

### Example 2: CI/CD Pipeline Integration

```yaml
# .github/workflows/plantuml.yml
name: Generate PlantUML Documentation

on:
  push:
    branches: [ main ]
    paths:
      - 'diagrams/**/*.puml'

jobs:
  generate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      
      - name: Generate PlantUML documentation
        run: |
          docker run --rm \
            -v $(pwd)/diagrams:/input \
            -v $(pwd)/docs:/output \
            puml-generator process
      
      - name: Publish to Azure DevOps
        env:
          AZURE_PAT: ${{ secrets.AZURE_DEVOPS_PAT }}
        run: |
          docker run --rm \
            -v $(pwd)/docs:/output \
            -e AZURE_DEVOPS_ORG=${{ vars.AZURE_ORG }} \
            -e AZURE_DEVOPS_PROJECT=${{ vars.AZURE_PROJECT }} \
            -e AZURE_DEVOPS_WIKI_ID=${{ vars.AZURE_WIKI_ID }} \
            -e AZURE_DEVOPS_PAT=$AZURE_PAT \
            puml-generator python3 /app/azure_wiki_publisher.py /output \
              --organization ${{ vars.AZURE_ORG }} \
              --project ${{ vars.AZURE_PROJECT }} \
              --wiki-id ${{ vars.AZURE_WIKI_ID }}
```

### Example 3: Using Docker Compose for Development

```yaml
# docker-compose.yml
version: '3.8'

services:
  puml-generator:
    build: .
    ports:
      - "8080:8080"
    volumes:
      - ./my-diagrams:/input
      - ./docs:/output
    environment:
      - INPUT_DIR=/input
      - OUTPUT_DIR=/output
      - PORT=8080
    command: serve
```

Then run:
```bash
docker-compose up -d
docker-compose logs -f
```

## Best Practices

1. **Organize Your Files**: Keep related diagrams in subdirectories for better organization
2. **Use Descriptive Names**: Name your PlantUML files clearly to make the generated index useful
3. **Version Control**: Keep your PlantUML source files in version control
4. **Regular Updates**: Regenerate documentation when diagrams change
5. **Security**: Never commit PAT tokens to version control; use environment variables or secrets management

## Additional Resources

- [PlantUML Official Documentation](https://plantuml.com/)
- [Azure DevOps Wiki Documentation](https://docs.microsoft.com/en-us/azure/devops/project/wiki/)
- [Docker Documentation](https://docs.docker.com/)
