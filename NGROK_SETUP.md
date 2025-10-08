# Setting Up ngrok with Fruit Store MCP Server

This guide will help you expose your MCP server to the internet using ngrok.

## Prerequisites

✅ Python 3.10 virtual environment is set up  
✅ MCP dependencies are installed  
✅ ngrok is installed on your system  

## Quick Start

### Step 1: Start the SSE Server

Open a terminal and run:

```bash
cd /Users/adarsh/Documents/Git
./start_sse_server.sh
```

Or manually:

```bash
source venv/bin/activate
python fruit_store_server_sse.py --host 0.0.0.0 --port 8000
```

You should see output like:
```
🍎 Fruit Store MCP Server starting on http://0.0.0.0:8000
📡 SSE endpoint: http://0.0.0.0:8000/sse
📦 Initial inventory: Apples=100, Oranges=150, Bananas=200

Waiting for connections...
INFO:     Started server process [xxxxx]
INFO:     Uvicorn running on http://0.0.0.0:8000
```

**Keep this terminal open!**

### Step 2: Create ngrok Tunnel

Open a **NEW** terminal window and run:

```bash
cd /Users/adarsh/Documents/Git
./setup_ngrok.sh
```

Or manually:

```bash
ngrok http 8000
```

You should see output like:
```
ngrok                                                          

Session Status                online                          
Account                       your-account                    
Version                       x.x.x                          
Region                        United States (us)             
Latency                       -                              
Web Interface                 http://127.0.0.1:4040          
Forwarding                    https://xxxx-xx-xx.ngrok-free.app -> http://localhost:8000

Connections                   ttl     opn     rt1     rt5     p50     p90
                              0       0       0.00    0.00    0.00    0.00
```

**Copy the Forwarding URL** (e.g., `https://xxxx-xx-xx.ngrok-free.app`)

### Step 3: Your Public Endpoints

Your MCP server is now accessible via:

- **SSE Endpoint**: `https://xxxx-xx-xx.ngrok-free.app/sse`
- **Message Endpoint**: `https://xxxx-xx-xx.ngrok-free.app/messages/`

### Step 4: Connect from MCP Clients

Use the SSE endpoint URL in your MCP client configuration. For example, in Claude Desktop or other MCP clients, configure:

```json
{
  "mcpServers": {
    "fruit-store": {
      "url": "https://xxxx-xx-xx.ngrok-free.app/sse",
      "transport": "sse"
    }
  }
}
```

Replace `xxxx-xx-xx.ngrok-free.app` with your actual ngrok URL.

## Testing the Connection

You can test your SSE endpoint with curl:

```bash
curl -N https://your-ngrok-url.ngrok-free.app/sse
```

You should see SSE events streaming.

## Available MCP Tools

Once connected, your clients will have access to:

1. **get_inventory** - View all fruit stock levels
2. **check_fruit** - Check a specific fruit's inventory
3. **place_order** - Order fruits with quantity
4. **get_orders** - View order history

## Troubleshooting

### Server won't start
- Make sure no other process is using port 8000
- Try a different port: `python fruit_store_server_sse.py --port 8001`

### ngrok tunnel fails
- Ensure ngrok is authenticated: `ngrok authtoken YOUR_TOKEN`
- Check your ngrok account limits (free tier has restrictions)

### Can't connect from clients
- Verify both terminals (server and ngrok) are still running
- Check the ngrok URL is correct and HTTPS
- Some networks may block SSE connections

### ngrok free tier warning page
- Free tier ngrok URLs show a warning page before connecting
- Click "Visit Site" to proceed
- Consider upgrading to a paid plan for production use

## Custom Port

To use a different port:

**Server:**
```bash
python fruit_store_server_sse.py --port 8080
```

**ngrok:**
```bash
ngrok http 8080
```

## Stopping the Server

1. In the server terminal, press `Ctrl+C`
2. In the ngrok terminal, press `Ctrl+C`

## ngrok Web Interface

ngrok provides a local web interface to monitor requests:

- URL: http://127.0.0.1:4040
- View all HTTP requests and responses
- Replay requests for debugging
- See connection statistics

## Security Notes

⚠️ **Important Security Considerations:**

1. **Authentication**: This server has no authentication. Anyone with the URL can access it.
2. **Rate Limiting**: No rate limiting is implemented.
3. **Data Persistence**: Inventory resets when the server restarts.
4. **Production Use**: Not recommended for production without proper security measures.

For production use, consider:
- Adding authentication/authorization
- Implementing rate limiting
- Using persistent storage (database)
- Setting up proper logging and monitoring
- Using a custom domain with SSL

## Next Steps

- Integrate with Claude Desktop
- Build a web UI for the fruit store
- Add more fruits and features
- Implement authentication
- Add persistent storage

Happy fruit selling! 🍎🍊🍌

