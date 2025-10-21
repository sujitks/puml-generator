#!/bin/bash
set -e

# Default values
INPUT_DIR=${INPUT_DIR:-/input}
OUTPUT_DIR=${OUTPUT_DIR:-/output}

# Function to process PlantUML files
process() {
    echo "Processing PlantUML files from: $INPUT_DIR"
    python3 /app/puml_processor.py "$INPUT_DIR" -o "$OUTPUT_DIR"
}

# Function to serve documentation
serve() {
    echo "Starting web server to serve documentation..."
    python3 /app/server.py
}

# Function to publish to Azure DevOps
publish() {
    if [ -z "$AZURE_DEVOPS_ORG" ] || [ -z "$AZURE_DEVOPS_PROJECT" ] || [ -z "$AZURE_DEVOPS_WIKI_ID" ]; then
        echo "Error: Azure DevOps configuration required"
        echo "Set: AZURE_DEVOPS_ORG, AZURE_DEVOPS_PROJECT, AZURE_DEVOPS_WIKI_ID, AZURE_DEVOPS_PAT"
        exit 1
    fi
    
    echo "Publishing to Azure DevOps wiki..."
    python3 /app/azure_wiki_publisher.py "$OUTPUT_DIR" \
        --organization "$AZURE_DEVOPS_ORG" \
        --project "$AZURE_DEVOPS_PROJECT" \
        --wiki-id "$AZURE_DEVOPS_WIKI_ID" \
        --wiki-path "${AZURE_DEVOPS_WIKI_PATH:-/PlantUML}"
}

# Main command handler
case "$1" in
    process)
        process
        ;;
    serve)
        # Process first, then serve
        process
        serve
        ;;
    publish)
        # Process first, then publish
        process
        publish
        ;;
    process-and-publish)
        # Process, then publish, then serve
        process
        publish
        serve
        ;;
    *)
        # Default: run custom command
        exec "$@"
        ;;
esac
