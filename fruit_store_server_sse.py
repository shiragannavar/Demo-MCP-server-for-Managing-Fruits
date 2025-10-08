#!/usr/bin/env python3
"""
Simple MCP Server for Fruit Store (SSE Mode)
Handles inventory management and order placement for apples, oranges, and bananas.
Runs as HTTP server with SSE transport for remote access via ngrok.
"""

import asyncio
import json
import argparse
from typing import Any
from mcp.server import Server
from mcp.server.sse import SseServerTransport
from starlette.applications import Starlette
from starlette.routing import Mount, Route
from starlette.responses import Response
from mcp.types import Tool, TextContent
import uvicorn

# Initial inventory
inventory = {
    "apple": 100,
    "orange": 150,
    "banana": 200
}

# Order history
orders = []

# Initialize MCP server
app = Server("fruit-store-server")


@app.list_tools()
async def list_tools() -> list[Tool]:
    """List available tools for the fruit store."""
    return [
        Tool(
            name="get_inventory",
            description="Get current inventory levels for all fruits (apples, oranges, bananas)",
            inputSchema={
                "type": "object",
                "properties": {},
                "required": []
            }
        ),
        Tool(
            name="check_fruit",
            description="Check inventory level for a specific fruit",
            inputSchema={
                "type": "object",
                "properties": {
                    "fruit": {
                        "type": "string",
                        "enum": ["apple", "orange", "banana"],
                        "description": "The fruit to check (apple, orange, or banana)"
                    }
                },
                "required": ["fruit"]
            }
        ),
        Tool(
            name="place_order",
            description="Place an order for fruits. Reduces inventory if sufficient stock is available.",
            inputSchema={
                "type": "object",
                "properties": {
                    "fruit": {
                        "type": "string",
                        "enum": ["apple", "orange", "banana"],
                        "description": "The fruit to order (apple, orange, or banana)"
                    },
                    "quantity": {
                        "type": "integer",
                        "minimum": 1,
                        "description": "Quantity to order (must be positive)"
                    }
                },
                "required": ["fruit", "quantity"]
            }
        ),
        Tool(
            name="get_orders",
            description="Get list of all placed orders",
            inputSchema={
                "type": "object",
                "properties": {},
                "required": []
            }
        )
    ]


@app.call_tool()
async def call_tool(name: str, arguments: Any) -> list[TextContent]:
    """Handle tool calls for the fruit store."""
    
    if name == "get_inventory":
        result = {
            "inventory": inventory,
            "message": "Current inventory levels for all fruits"
        }
        return [TextContent(
            type="text",
            text=json.dumps(result, indent=2)
        )]
    
    elif name == "check_fruit":
        fruit = arguments.get("fruit", "").lower()
        
        if fruit not in inventory:
            return [TextContent(
                type="text",
                text=json.dumps({
                    "error": f"Invalid fruit: {fruit}. Available fruits: apple, orange, banana"
                }, indent=2)
            )]
        
        result = {
            "fruit": fruit,
            "available": inventory[fruit],
            "message": f"{fruit.capitalize()} inventory: {inventory[fruit]} units"
        }
        return [TextContent(
            type="text",
            text=json.dumps(result, indent=2)
        )]
    
    elif name == "place_order":
        fruit = arguments.get("fruit", "").lower()
        quantity = arguments.get("quantity", 0)
        
        # Validation
        if fruit not in inventory:
            return [TextContent(
                type="text",
                text=json.dumps({
                    "error": f"Invalid fruit: {fruit}. Available fruits: apple, orange, banana"
                }, indent=2)
            )]
        
        if quantity <= 0:
            return [TextContent(
                type="text",
                text=json.dumps({
                    "error": "Quantity must be positive"
                }, indent=2)
            )]
        
        if inventory[fruit] < quantity:
            return [TextContent(
                type="text",
                text=json.dumps({
                    "error": f"Insufficient inventory. Requested: {quantity}, Available: {inventory[fruit]}",
                    "fruit": fruit,
                    "requested": quantity,
                    "available": inventory[fruit]
                }, indent=2)
            )]
        
        # Process order
        inventory[fruit] -= quantity
        order = {
            "order_id": len(orders) + 1,
            "fruit": fruit,
            "quantity": quantity,
            "status": "completed"
        }
        orders.append(order)
        
        result = {
            "success": True,
            "order": order,
            "remaining_inventory": inventory[fruit],
            "message": f"Order placed successfully! {quantity} {fruit}(s) ordered. Remaining: {inventory[fruit]}"
        }
        return [TextContent(
            type="text",
            text=json.dumps(result, indent=2)
        )]
    
    elif name == "get_orders":
        result = {
            "total_orders": len(orders),
            "orders": orders,
            "message": f"Total orders placed: {len(orders)}"
        }
        return [TextContent(
            type="text",
            text=json.dumps(result, indent=2)
        )]
    
    else:
        return [TextContent(
            type="text",
            text=json.dumps({
                "error": f"Unknown tool: {name}"
            }, indent=2)
        )]


# Create SSE transport at /messages/ endpoint
sse_transport = SseServerTransport("/messages/")


# Define SSE handler
async def handle_sse(request):
    """Handle SSE connections for MCP."""
    async with sse_transport.connect_sse(
        request.scope, request.receive, request._send
    ) as streams:
        await app.run(
            streams[0], streams[1], app.create_initialization_options()
        )
    # Return empty response to avoid NoneType error
    return Response()


# Create Starlette application with routes
starlette_app = Starlette(
    routes=[
        Route("/sse", endpoint=handle_sse, methods=["GET"]),
        Mount("/messages/", app=sse_transport.handle_post_message),
    ]
)


def main():
    """Run the MCP server with SSE transport."""
    parser = argparse.ArgumentParser(description="Fruit Store MCP Server (SSE)")
    parser.add_argument("--host", default="0.0.0.0", help="Host to bind to")
    parser.add_argument("--port", type=int, default=8000, help="Port to bind to")
    args = parser.parse_args()
    
    print(f"🍎 Fruit Store MCP Server starting on http://{args.host}:{args.port}")
    print(f"📡 SSE endpoint: http://{args.host}:{args.port}/sse")
    print(f"📦 Initial inventory: Apples={inventory['apple']}, Oranges={inventory['orange']}, Bananas={inventory['banana']}")
    print("\nWaiting for connections...")
    
    uvicorn.run(
        starlette_app,
        host=args.host,
        port=args.port,
        log_level="info"
    )


if __name__ == "__main__":
    main()

