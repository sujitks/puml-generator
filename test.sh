#!/bin/bash
# Test script to validate PlantUML generator functionality

set -e

echo "=== PlantUML Generator Test Suite ==="
echo ""

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Test 1: Build Docker image
echo "Test 1: Building Docker image..."
if docker build -t puml-generator:test . > /dev/null 2>&1; then
    echo -e "${GREEN}✓ Docker build successful${NC}"
else
    echo -e "${RED}✗ Docker build failed${NC}"
    exit 1
fi
echo ""

# Test 2: Process example files
echo "Test 2: Processing example PlantUML files..."
sudo rm -rf test-output
if docker run --rm \
    -v $(pwd)/examples:/input \
    -v $(pwd)/test-output:/output \
    puml-generator:test process > /dev/null 2>&1; then
    echo -e "${GREEN}✓ Processing successful${NC}"
else
    echo -e "${RED}✗ Processing failed${NC}"
    exit 1
fi
echo ""

# Test 3: Validate output files
echo "Test 3: Validating generated files..."
EXPECTED_FILES=(
    "test-output/index.md"
    "test-output/architecture/web-app-architecture.png"
    "test-output/architecture/web-app-architecture.md"
    "test-output/sequences/login-flow.png"
    "test-output/sequences/login-flow.md"
    "test-output/sequences/request-processing.png"
    "test-output/sequences/request-processing.md"
)

ALL_FILES_EXIST=true
for file in "${EXPECTED_FILES[@]}"; do
    if [ -f "$file" ]; then
        echo -e "${GREEN}✓ Found: $file${NC}"
    else
        echo -e "${RED}✗ Missing: $file${NC}"
        ALL_FILES_EXIST=false
    fi
done
echo ""

if [ "$ALL_FILES_EXIST" = false ]; then
    echo -e "${RED}✗ Some expected files are missing${NC}"
    exit 1
fi

# Test 4: Validate PNG files
echo "Test 4: Validating PNG files..."
for png in test-output/**/*.png; do
    if [ -f "$png" ]; then
        if file "$png" | grep -q "PNG image data"; then
            echo -e "${GREEN}✓ Valid PNG: $png${NC}"
        else
            echo -e "${RED}✗ Invalid PNG: $png${NC}"
            exit 1
        fi
    fi
done
echo ""

# Test 5: Start and test web server
echo "Test 5: Testing web server..."
CONTAINER_ID=$(docker run -d \
    -v $(pwd)/test-output:/output \
    -p 18080:8080 \
    -e SERVE_DIR=/output \
    puml-generator:test python3 /app/server.py)

# Wait for server to start
sleep 2

# Test HTTP endpoint
if curl -s http://localhost:18080/index.md > /dev/null; then
    echo -e "${GREEN}✓ Web server is responding${NC}"
else
    echo -e "${RED}✗ Web server is not responding${NC}"
    docker stop $CONTAINER_ID > /dev/null
    docker rm $CONTAINER_ID > /dev/null
    exit 1
fi

# Cleanup
docker stop $CONTAINER_ID > /dev/null
docker rm $CONTAINER_ID > /dev/null
echo ""

# Test 6: Validate markdown content
echo "Test 6: Validating markdown content..."
if grep -q "PlantUML Documentation Index" test-output/index.md; then
    echo -e "${GREEN}✓ Index markdown has correct header${NC}"
else
    echo -e "${RED}✗ Index markdown is invalid${NC}"
    exit 1
fi

if grep -q "web-app-architecture" test-output/index.md; then
    echo -e "${GREEN}✓ Index contains expected diagram links${NC}"
else
    echo -e "${RED}✗ Index missing diagram links${NC}"
    exit 1
fi
echo ""

# Cleanup
sudo rm -rf test-output

echo -e "${GREEN}=== All tests passed! ===${NC}"
echo ""
echo "You can now use the puml-generator Docker image:"
echo "  docker run -d -v /path/to/puml:/input -v /path/to/output:/output -p 8080:8080 puml-generator:test serve"
