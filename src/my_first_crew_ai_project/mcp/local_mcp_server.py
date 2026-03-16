import asyncio
from mcp.server.models import InitializationOptions
import mcp.types as types
from mcp.server import NotificationOptions, Server
from mcp.server.stdio import stdio_server

# Create a server instance
server = Server("my-local-mcp-server")

@server.list_tools()
async def handle_list_tools() -> list[types.Tool]:
    """
    List available tools.
    Each tool specifies its arguments using JSON Schema.
    """
    return [
        types.Tool(
            name="get_project_info",
            description="Get information about the current YouTube Content Factory project",
            inputSchema={
                "type": "object",
                "properties": {},
            },
        ),
        types.Tool(
            name="calculate_video_metrics",
            description="Calculate engagement metrics for a video",
            inputSchema={
                "type": "object",
                "properties": {
                    "views": {"type": "integer"},
                    "likes": {"type": "integer"},
                    "comments": {"type": "integer"},
                },
                "required": ["views", "likes"],
            },
        ),
    ]

@server.call_tool()
async def handle_call_tool(
    name: str, arguments: dict | None
) -> list[types.TextContent | types.ImageContent | types.EmbeddedResource]:
    """
    Handle tool calls.
    This is where you implement the logic for your tools.
    """
    if name == "get_project_info":
        return [
            types.TextContent(
                type="text",
                text="YouTube Content Factory v0.1.0 - A CrewAI project to automate YouTube content creation."
            )
        ]
    elif name == "calculate_video_metrics":
        if not arguments:
            raise ValueError("Missing arguments")
        
        views = arguments.get("views", 0)
        likes = arguments.get("likes", 0)
        comments = arguments.get("comments", 0)
        
        # Simple engagement rate calculation
        engagement_rate = ((likes + comments) / views) * 100 if views > 0 else 0
        
        return [
            types.TextContent(
                type="text",
                text=f"Metrics Summary:\n- Views: {views}\n- Likes: {likes}\n- Comments: {comments}\n- Engagement Rate: {engagement_rate:.2f}%"
            )
        ]
    else:
        raise ValueError(f"Unknown tool: {name}")

async def main():
    # Run the server using stdin/stdout streams
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="my-local-mcp-server",
                server_version="0.1.0",
                capabilities=server.get_capabilities(
                    notification_options=NotificationOptions(),
                    experimental_capabilities={},
                ),
            ),
        )

if __name__ == "__main__":
    asyncio.run(main())
