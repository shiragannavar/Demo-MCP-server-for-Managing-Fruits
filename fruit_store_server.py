#!/usr/bin/env python3
"""
Simple MCP Server for Fruit Store
Handles inventory management and order placement for apples, oranges, and bananas.
"""

import asyncio
import json
from typing import Any
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent

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


async def main():
    """Run the MCP server."""
    async with stdio_server() as (read_stream, write_stream):
        await app.run(
            read_stream,
            write_stream,
            app.create_initialization_options()
        )


if __name__ == "__main__":
    asyncio.run(main())

