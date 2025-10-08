# Fruit Store MCP Server

A simple Model Context Protocol (MCP) server for managing a fruit store inventory and orders.

## Features

- **Inventory Management**: Track inventory for apples, oranges, and bananas
- **Check Inventory**: View current stock levels for all fruits or specific fruits
- **Place Orders**: Order fruits with automatic inventory deduction
- **Order History**: View all placed orders

## Setup

### 1. Activate the virtual environment

```bash
source venv/bin/activate
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

## Usage

### Running the Server

The MCP server supports two modes:

#### 1. **Stdio Mode** (Local - for Claude Desktop)

```bash
python fruit_store_server.py
```

#### 2. **SSE Mode** (Remote - for ngrok/web access)

Start the server:
```bash
./start_sse_server.sh
# Or specify a custom port:
./start_sse_server.sh 8080
```

Or manually:
```bash
source venv/bin/activate
python fruit_store_server_sse.py --host 0.0.0.0 --port 8000
```

### Available Tools

#### 1. `get_inventory`
Get current inventory levels for all fruits.

**Example Response:**
```json
{
  "inventory": {
    "apple": 100,
    "orange": 150,
    "banana": 200
  },
  "message": "Current inventory levels for all fruits"
}
```

#### 2. `check_fruit`
Check inventory level for a specific fruit.

**Parameters:**
- `fruit` (string, required): The fruit to check (apple, orange, or banana)

**Example Response:**
```json
{
  "fruit": "apple",
  "available": 100,
  "message": "Apple inventory: 100 units"
}
```

#### 3. `place_order`
Place an order for fruits. Reduces inventory if sufficient stock is available.

**Parameters:**
- `fruit` (string, required): The fruit to order (apple, orange, or banana)
- `quantity` (integer, required): Quantity to order (must be positive)

**Example Response:**
```json
{
  "success": true,
  "order": {
    "order_id": 1,
    "fruit": "apple",
    "quantity": 10,
    "status": "completed"
  },
  "remaining_inventory": 90,
  "message": "Order placed successfully! 10 apple(s) ordered. Remaining: 90"
}
```

#### 4. `get_orders`
Get list of all placed orders.

**Example Response:**
```json
{
  "total_orders": 1,
  "orders": [
    {
      "order_id": 1,
      "fruit": "apple",
      "quantity": 10,
      "status": "completed"
    }
  ],
  "message": "Total orders placed: 1"
}
```

## Integration with Claude Desktop

To use this MCP server with Claude Desktop:

1. Open Claude Desktop configuration file:
   - macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`

2. Add the server configuration:

```json
{
  "mcpServers": {
    "fruit-store": {
      "command": "/Users/adarsh/Documents/Git/venv/bin/python",
      "args": [
        "/Users/adarsh/Documents/Git/fruit_store_server.py"
      ]
    }
  }
}
```

3. Restart Claude Desktop

4. The fruit store tools will be available in your conversations!

## Initial Inventory

- Apples: 100 units
- Oranges: 150 units  
- Bananas: 200 units

## Error Handling

The server handles various error cases:
- Invalid fruit names
- Negative or zero quantities
- Insufficient inventory
- Unknown tool calls

## Exposing via ngrok

To make your MCP server accessible remotely via ngrok:

### Step 1: Start the SSE Server

In one terminal:
```bash
./start_sse_server.sh
```

The server will start on `http://localhost:8000` with SSE endpoint at `/sse`

### Step 2: Create ngrok Tunnel

In another terminal:
```bash
./setup_ngrok.sh
# Or specify a custom port:
./setup_ngrok.sh 8080
```

Or manually:
```bash
ngrok http 8000
```

### Step 3: Use Your Public URL

ngrok will provide you with a public URL like: `https://xxxx-xx-xx-xx-xx.ngrok-free.app`

Your MCP SSE endpoint will be available at:
```
https://xxxx-xx-xx-xx-xx.ngrok-free.app/sse
```

### Step 4: Connect MCP Clients

Use this URL in your MCP client configuration to connect remotely to your fruit store server!

## Development

### Project Structure

```
.
├── README.md
├── requirements.txt
├── fruit_store_server.py          # Stdio mode server
├── fruit_store_server_sse.py      # SSE/HTTP mode server
├── start_sse_server.sh            # Helper script to start SSE server
├── setup_ngrok.sh                 # Helper script to setup ngrok
├── mcp_config.json
└── venv/
```

### Extending the Server

To add new fruits or features, modify the `inventory` dictionary and update the tool schemas in both `fruit_store_server.py` and `fruit_store_server_sse.py`.

