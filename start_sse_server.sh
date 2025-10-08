#!/bin/bash
# Start the Fruit Store MCP Server in SSE mode

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${GREEN}🍎 Starting Fruit Store MCP Server (SSE Mode)${NC}"
echo ""

# Activate virtual environment
source venv/bin/activate

# Default port
PORT=${1:-8000}

echo -e "${BLUE}Server will run on: http://localhost:$PORT${NC}"
echo -e "${BLUE}SSE endpoint: http://localhost:$PORT/sse${NC}"
echo ""

# Start the server
python fruit_store_server_sse.py --host 0.0.0.0 --port $PORT

