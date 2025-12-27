# AUTOMATION_MIGRATION.md

## 🔄 Migration from N8N to LangGraph

This document details the migration of automation workflows from N8N (external tool) to code-owned LangGraph implementation, making automation version-controlled, testable, and maintainable.

## 📋 Migration Overview

### Before: N8N Workflows
- External automation tool dependency
- Workflows stored as JSON configurations
- Not version-controlled in codebase
- Difficult to test and maintain

### After: LangGraph Implementation
- Code-owned automation in version control
- Testable workflow definitions
- Maintainable and extensible
- Integrated directly in backend

## 🏗️ New Architecture

### Directory Structure
```
src/
└── langgraph/
    ├── flows/
    │   ├── judge_flow.py          # Judge scoring workflow
    │   ├── mentor_flow.py         # Mentor interaction workflow  
    │   ├── reminder_flow.py       # Deadline reminder workflow
    │   └── team_registration_flow.py # Team registration workflow
    ├── runner.py                 # Workflow execution runner
    ├── manager.py                # Workflow registry and management
    └── __init__.py
```

### API Endpoints
- `POST /flows/{flow_name}` - Generic flow execution endpoint
- `POST /flows/judge` - Judge flow execution
- `POST /flows/mentor` - Mentor flow execution  
- `POST /flows/reminder` - Reminder flow execution
- `POST /flows/team_registration` - Team registration flow execution

## 🔄 Workflow Migrations

### 1. Judge Flow
**Purpose**: Automated judging of submissions
**Input**: Project submission data
**Steps**:
1. Assign judge agent
2. Score rubric criteria using multi-agent system
3. Persist scores to database
4. Log provenance of judging process

### 2. Mentor Flow
**Purpose**: Automated mentor interaction
**Input**: Participant question
**Steps**:
1. Validate input
2. Route to mentor agent
3. Generate reply using AI
4. Store interaction in database

### 3. Reminder Flow
**Purpose**: Automated deadline reminders
**Input**: Deadline configuration
**Steps**:
1. Fetch teams requiring reminders
2. Send reminder notifications
3. Log delivery confirmation

### 4. Team Registration Flow
**Purpose**: Automated team registration
**Input**: Team registration data
**Steps**:
1. Validate registration data
2. Register team in database
3. Log registration event

## 🔧 Technical Implementation

### Dependencies
- `langgraph` - Workflow orchestration
- `tenacity` - Retry logic
- `httpx` - Async HTTP client

### Core Components

#### State Management
Each workflow uses LangGraph's StateGraph for state management:
```python
from langgraph.graph import StateGraph

g = StateGraph(dict)
g.add_node("node_name", node_function)
g.add_edge("source_node", "target_node")
```

#### Flow Registry
Flows are registered in `src/langgraph/manager.py`:
```python
FLOW_REGISTRY = {
    "judge": build_judge_flow(),
    "mentor": build_mentor_flow(),
    "reminder": build_reminder_flow(),
    "team_registration": build_team_registration_flow(),
}
```

## 🧪 Testing

### Unit Tests
Each flow component has unit test coverage:
- Node function validation
- State transition verification
- Error handling testing

### Integration Tests
- End-to-end flow execution
- Database persistence verification
- Provenance logging validation

## 🚀 Deployment

### Environment Variables
- `OPENAI_API_KEY` - For AI-powered mentor interactions
- `NOTIFIER_URL` - For notification delivery

### Health Checks
- Flow registry validation
- Database connectivity verification
- External API availability checks

## 📊 Benefits Achieved

✅ **Version Control**: All workflows in Git repository
✅ **Testability**: Unit and integration tests for all flows
✅ **Maintainability**: Code-based workflow definitions
✅ **Extensibility**: Easy to add new workflow types
✅ **Observability**: Comprehensive logging and monitoring
✅ **Reliability**: Built-in retry logic and error handling

## 🔄 Migration Path

### Old N8N Endpoints
- `POST /admin/webhook/hackaverse/registration` - Now uses LangGraph flow internally

### New LangGraph Endpoints
- `POST /flows/{flow_name}` - Primary workflow execution
- Individual flow endpoints maintained for backward compatibility

## 📈 Future Enhancements

- Advanced workflow monitoring and metrics
- Dynamic workflow configuration
- A/B testing for workflow optimization
- Advanced error recovery mechanisms