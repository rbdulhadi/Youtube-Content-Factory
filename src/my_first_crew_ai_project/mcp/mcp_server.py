from crewai_tools import MCPServerAdapter, ScrapeWebsiteTool
from mcp import StdioServerParameters
import os
import subprocess
import logging


def can_start_mcp() -> bool:
    """
    Check if MCP is enabled and any server can be started.

    Returns:
        bool: True if MCP tools can be loaded, False otherwise
    """
    logger = logging.getLogger(__name__)
    
    # Check if MCP is enabled via environment variable
    mcp_enabled = os.getenv('MCP_ENABLED', 'true').lower() == 'true'
    
    if not mcp_enabled:
        logger.warning("MCP is disabled via MCP_ENABLED environment variable")
        return False
    
    return True


def get_mcp_tools():
    """
    Initialize MCP server adapter for YouTube Content Factory.

    Using YouTube MCP server to search for trending videos, popular titles,
    and successful content patterns. This helps the Trend Scout discover
    what's working on YouTube in the target niche.

    To install:
    - YouTube MCP server: uv tool install git+https://github.com/sparfenyuk/mcp-youtube

    You need a YouTube Data API key in your .env file:
    - YOUTUBE_API_KEY=your_api_key_here

    Alternative MCP servers you can add:
    - arXiv MCP server (for academic research)
    - Web search MCP server
    - Other content discovery servers
    
    To build your own MCP server:
    1. Create a Python file (e.g., `local_mcp_server.py`) using the `mcp` SDK.
    2. Define your tools and logic within that file.
    3. Add it to the `server_params` list in `get_mcp_tools()`.
    """
    logger = logging.getLogger(__name__)
    logger.info("Initializing MCP tools...")

    # Create server parameters
    server_params = []

    # 1. Add YouTube MCP server (remote tool)
    youtube_api_key = os.getenv('YOUTUBE_API_KEY')
    if youtube_api_key:
        logger.info("✓ YOUTUBE_API_KEY found. Adding YouTube MCP server.")
        server_params.append(
            StdioServerParameters(
                command="uv",
                args=["tool", "run", "mcp-youtube", "run"],
                env={"YOUTUBE_API_KEY": youtube_api_key}
            )
        )
    else:
        logger.warning("YOUTUBE_API_KEY not found. Skipping YouTube MCP server.")

    # 2. Add our own local MCP server
    logger.info("Adding local MCP server...")
    # Get the absolute path to our local server file
    current_dir = os.path.dirname(os.path.abspath(__file__))
    local_server_path = os.path.join(current_dir, "local_mcp_server.py")
    
    server_params.append(
        StdioServerParameters(
            command="python",
            args=[local_server_path],
            env=os.environ.copy()
        )
    )

    if not server_params:
        logger.error("No MCP servers configured")
        return []

    logger.info(f"Creating MCPServerAdapter with {len(server_params)} servers...")
    adapter = MCPServerAdapter(server_params)
    logger.info(f"✓ MCPServerAdapter created successfully with {len(adapter.tools)} tools")

    return adapter.tools


def get_trend_scout_tools():
    """
    Get tools for the Trend Scout agent with MCP support.

    Returns a list of tools with MCP YouTube tools if available,
    or falls back to ScrapeWebsiteTool only.

    Returns:
        list: List of tools for the Trend Scout agent
    """
    logger = logging.getLogger(__name__)
    logger.info("=" * 60)
    logger.info("Getting tools for Trend Scout agent...")
    logger.info("=" * 60)

    tools = [ScrapeWebsiteTool()]
    logger.info("✓ Added ScrapeWebsiteTool to tools list")

    if not can_start_mcp():
        logger.warning("⚠ MCP disabled - using ScrapeWebsiteTool only")
        logger.info(f"Total tools available: {len(tools)}")
        logger.info("=" * 60)
        return tools

    try:
        logger.info("Attempting to load MCP tools...")
        mcp_tools = get_mcp_tools()
        tools.extend(mcp_tools)
        logger.info("=" * 60)
        logger.info(f"✓ SUCCESS: Loaded {len(mcp_tools)} MCP tools")
        logger.info(f"MCP tool names: {[type(t).__name__ for t in mcp_tools]}")
        logger.info(f"Total tools available: {len(tools)} (1 ScrapeWebsiteTool + {len(mcp_tools)} MCP tools)")
        logger.info("=" * 60)
    except Exception as exc:
        logger.error("=" * 60)
        logger.error(f"✗ FAILED to load MCP tools: {exc}")
        logger.error("Continuing with web scraping only")
        logger.info(f"Total tools available: {len(tools)}")
        logger.error("=" * 60)

    return tools