from crewai_tools import MCPServerAdapter, ScrapeWebsiteTool
from mcp import StdioServerParameters
import os
import subprocess
import logging


def can_start_mcp_youtube() -> bool:
    """
    Check if mcp-youtube tool is available and runnable.

    Returns:
        bool: True if mcp-youtube can be started, False otherwise
    """
    logger = logging.getLogger(__name__)
    logger.info("Checking if mcp-youtube is available...")

    # Check if MCP is enabled via environment variable
    mcp_enabled = os.getenv('MCP_ENABLED', 'true').lower() == 'true'
    logger.info(f"MCP_ENABLED environment variable: {os.getenv('MCP_ENABLED', 'true')} (evaluated as: {mcp_enabled})")

    if not mcp_enabled:
        logger.warning("MCP is disabled via MCP_ENABLED environment variable")
        return False

    # Check if mcp-youtube command is available
    logger.info("Running command: uv tool run mcp-youtube --help")
    try:
        check = subprocess.run(
            ["uv", "tool", "run", "mcp-youtube", "--help"],
            capture_output=True,
            text=True,
            timeout=8,
            check=False,
        )

        logger.info(f"Command exit code: {check.returncode}")

        if check.returncode == 0:
            logger.info("✓ mcp-youtube is available and runnable")
            return True
        else:
            details = (check.stderr or check.stdout).strip().splitlines()
            reason = details[0] if details else "unknown startup failure"
            logger.warning(
                "mcp-youtube is not runnable (%s). MCP tools disabled.",
                reason,
            )
            return False

    except Exception as exc:
        logger.warning(
            "Could not verify mcp-youtube startup (%s). MCP tools disabled.",
            exc,
        )
        return False


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
    """
    logger = logging.getLogger(__name__)
    logger.info("Initializing MCP tools...")

    youtube_api_key = os.getenv('YOUTUBE_API_KEY')
    if not youtube_api_key:
        logger.error("YOUTUBE_API_KEY not found in environment variables")
        raise ValueError("YOUTUBE_API_KEY not found in environment variables")

    logger.info("✓ YOUTUBE_API_KEY found")
    logger.info("Creating MCP server parameters for: uv tool run mcp-youtube run")

    server_params = [
        StdioServerParameters(
            command="uv",
            args=["tool", "run", "mcp-youtube", "run"],
            env={"YOUTUBE_API_KEY": youtube_api_key}
        )
        # Add more MCP servers here if needed
        # Example for arXiv (educational research):
        # StdioServerParameters(
        #     command="uv",
        #     args=[
        #         "tool",
        #         "run",
        #         "arxiv-mcp-server",
        #         "--storage-path",
        #         "./papers",
        #     ],
        # )
    ]

    logger.info("Creating MCPServerAdapter...")
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

    if not can_start_mcp_youtube():
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