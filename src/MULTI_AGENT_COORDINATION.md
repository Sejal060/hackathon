# Multi-Agent Coordination Feature

This directory contains the implementation of Step 5: Multi-Agent Coordination in the mcp_router.

## Structure

- `agents/` - Contains agent implementations
  - `base_agent.py` - Abstract base class for all agents
  - `judge_agent.py` - Judge agent implementation
  - `mentor_agent.py` - Mentor agent implementation
  - `system_agent.py` - System agent implementation
  - `default_agent.py` - Default agent implementation

- `mcp/` - Contains MCP routing components
  - `agent_registry.py` - Agent registry with load balancing support
  - `load_balancer.py` - Round-robin load balancer implementation

- `routes/mcp.py` - REST API endpoint for MCP routing

## Features

1. **Agent-to-agent forwarding** - Agents can forward tasks to other agents
2. **Role-based routing** - Routes to appropriate agent pool based on role
3. **Dynamic task switching** - Supports forwarding to different agents based on results
4. **Load balancing** - Multiple agents per role with round-robin distribution

## API Usage

```
POST /mcp/route
{
  "agent_type": "judge",
  "task": "score project"
}
```

## Testing

Run tests with:
```
python -m pytest tests/test_mcp_router.py -v
```