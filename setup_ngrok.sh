#!/bin/bash
# Setup ngrok tunnel for the MCP server

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Default port
PORT=${1:-8000}

echo -e "${GREEN}🌐 Setting up ngrok tunnel for Fruit Store MCP Server${NC}"
echo ""

# Check if ngrok is installed
if ! command -v ngrok &> /dev/null
then
    echo -e "${YELLOW}⚠️  ngrok not found in PATH${NC}"
    echo "Please ensure ngrok is installed and accessible"
    exit 1
fi

echo -e "${BLUE}Creating tunnel for port $PORT...${NC}"
echo ""
echo -e "${YELLOW}Keep this terminal open to maintain the tunnel!${NC}"
echo -e "${YELLOW}Your public URL will appear below:${NC}"
echo ""

# Start ngrok
ngrok http $PORT

