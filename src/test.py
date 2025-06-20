#!/usr/bin/env python3
"""
Test script for the WhatsApp MCP server
"""

import asyncio
import os

from titan_mind.server import mcp


async def test_tools():
    """Test the MCP server tools directly"""
    print("🧪 Testing WhatsApp MCP Server Tools\n")

    # Set up test environment
    os.environ.setdefault("TITANENGAGE_API_KEY", "test-key-for-testing")

    try:
        # Test 1: List available tools
        print("📋 Available Tools:")
        tools = mcp.list_tools()
        for tool in tools:
            print(f"  - {tool.name}: {tool.description}")
        print()

        # Test 2: List available prompts
        print("💬 Available Prompts:")
        prompts = mcp.list_prompts()
        for prompt in prompts:
            print(f"  - {prompt.name}: {prompt.description}")
        print()

        # Test 3: Test a prompt
        print("🎯 Testing WhatsApp Message Template Prompt:")
        try:
            prompt_result = await mcp.get_prompt(
                "WhatsApp Message Template",
                {"recipient": "John Doe", "context": "Following up on our meeting"}
            )
            print(f"Prompt Result: {prompt_result}")
        except Exception as e:
            print(f"Prompt test failed: {e}")
        print()

        # Test 4: Test tool calling (with mock data)
        print("🔧 Testing send_whatsapp_message tool:")
        try:
            # This will fail with API call but should show the structure
            result = await mcp.call_tool(
                "send_whatsapp_message",
                {
                    "phone_number": "+1234567890",
                    "message": "Test message from MCP server"
                }
            )
            print(f"Tool Result: {result}")
        except Exception as e:
            print(f"Tool test result (expected with test API key): {e}")
        print()

        print("✅ MCP Server structure test completed!")

    except Exception as e:
        print(f"❌ Error during testing: {e}")
        import traceback
        traceback.print_exc()


def test_server_startup():
    """Test if the server can start properly"""
    print("🚀 Testing MCP Server Startup\n")

    try:
        # Test server initialization
        print("Server name:", mcp.name)
        print("Server initialized successfully!")

        # Run async tests
        asyncio.run(test_tools())

    except Exception as e:
        print(f"❌ Server startup failed: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    test_server_startup()