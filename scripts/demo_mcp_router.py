#!/usr/bin/env python3
"""
Demo script to show the MCP router functionality
"""

import asyncio
import sys
import os

# Add the current directory to the path so we can import src modules
sys.path.insert(0, os.path.dirname(__file__))

from src.mcp_router import route_message

async def demo():
    print("MCP Router Demo")
    print("=" * 30)
    
    # Test judge routing
    print("\n1. Testing Judge Agent Routing:")
    result = await route_message("judge", {"task": "score project"})
    print(f"Result: {result}")
    
    # Test mentor routing
    print("\n2. Testing Mentor Agent Routing:")
    result = await route_message("mentor", {"task": "provide advice"})
    print(f"Result: {result}")
    
    # Test system routing
    print("\n3. Testing System Agent Routing:")
    result = await route_message("system", {"task": "perform maintenance"})
    print(f"Result: {result}")
    
    # Test default routing
    print("\n4. Testing Default Agent Routing:")
    result = await route_message("unknown", {"task": "handle unknown"})
    print(f"Result: {result}")
    
    # Test load balancing
    print("\n5. Testing Load Balancing (Judge Agents):")
    for i in range(3):
        result = await route_message("judge", {"task": f"score project {i+1}"})
        print(f"Request {i+1}: {result}")

if __name__ == "__main__":
    asyncio.run(demo())