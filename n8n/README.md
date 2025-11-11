# N8N Workflows for HackaVerse

This directory contains N8N workflows for automating various aspects of the HackaVerse hackathon platform.

## Workflows

### 1. Team Registration Workflow (`team_registration.json`)

Automates team registration by receiving webhook requests and forwarding them to the HackaVerse backend.

**Endpoints:**
- Webhook: `/webhook/hackaverse/registration`
- Backend: `/admin/webhook/hackaverse/registration`

**Payload:**
```json
{
  "team_name": "Team Name",
  "members": ["Member 1", "Member 2"],
  "project_title": "Project Title"
}
```

### 2. MentorBot Prompt Workflow (`mentorbot_prompt.json`)

Automates mentor requests by receiving prompts and forwarding them to the agent system.

**Endpoints:**
- Webhook: `/webhook/mentorbot/prompt`
- Backend: `/agent`

**Payload:**
```json
{
  "team_id": "team_123",
  "prompt": "How do I implement authentication?",
  "metadata": {
    "project_type": "web_app",
    "tech_stack": ["React", "Node.js"]
  }
}
```

### 3. Judging Reminder Workflow (`judging_reminder.json`)

Automatically reminds judges to review submissions on a scheduled basis.

**Schedule:** Every hour
**Action:** Sends email notification to judges

## Setup Instructions

1. Import the workflow JSON files into your N8N instance
2. Update the backend URLs in each workflow to point to your HackaVerse deployment
3. Activate the workflows
4. Configure any additional parameters (e.g., judge email addresses)

## Environment Variables

The workflows use configurable backend URLs. You can set these in the workflow parameters or use environment variables:

- `BACKEND_URL`: Base URL of your HackaVerse backend (e.g., https://ai-agent-x2iw.onrender.com)

## Testing

To test the workflows:

1. Start your HackaVerse backend
2. Activate the workflows in N8N
3. Send test payloads to the webhook endpoints
4. Verify that data is properly forwarded to the backend

Example test for team registration:
```bash
curl -X POST http://localhost:5678/webhook/hackaverse/registration \
  -H "Content-Type: application/json" \
  -d '{
    "team_name": "Test Team",
    "members": ["Alice", "Bob"],
    "project_title": "Test Project"
  }'
```

## Integration with HackaVerse

The workflows integrate with the following HackaVerse endpoints:

- `/admin/webhook/hackaverse/registration` - Team registration
- `/agent` - Agent prompts
- `/admin/submissions` - Submission retrieval (for judging)

All workflows are designed to be modular and can be extended or modified as needed.