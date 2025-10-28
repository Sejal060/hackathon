# N8N Workflows

This directory contains JSON workflow definitions for n8n automation.

## Workflows

### 1. Team Registration Workflow (`team_registration.json`)
- **Trigger**: Webhook
- **Action**: Sends registration data to the `/agent` endpoint
- **Purpose**: Automates team registration process

### 2. Judging Reminder Workflow (`judging_reminder.json`)
- **Trigger**: Schedule trigger (cron)
- **Action**: Sends email notifications to judges
- **Purpose**: Reminds judges to evaluate submissions

### 3. MentorBot Prompt Workflow (`mentorbot_prompt.json`)
- **Trigger**: Webhook
- **Action**: Sends mentor requests to the `/agent` endpoint
- **Purpose**: Provides automated mentor support

## How to Import Workflows

1. Open n8n (local installation or cloud version)
2. Go to **Settings** → **Import**
3. Paste the JSON content from any of the workflow files
4. Save and activate the workflow

## Endpoint Mappings

| Workflow | Trigger Type | Target Endpoint | Purpose |
|----------|--------------|-----------------|---------|
| `team_registration.json` | Webhook | `POST /agent` | Process team registration data |
| `judging_reminder.json` | Schedule | Email service | Send judging reminders |
| `mentorbot_prompt.json` | Webhook | `POST /agent` | Process mentor requests |

## Testing Workflows

To test these workflows without running n8n:

1. Use the test script `scripts/test_n8n_run.sh`
2. This script simulates webhook POSTs to your FastAPI endpoints
3. Check the responses to verify expected behavior

## Example Webhook URLs

After importing and activating workflows in n8n, you'll get webhook URLs like:

```
https://your-n8n-instance.web.app/webhook/team-registration
https://your-n8n-instance.web.app/webhook/mentor-request
```

## Example Payloads

### Team Registration Payload
```json
{
  "team_name": "Test Team",
  "members": ["Alice", "Bob", "Charlie"],
  "email": "test@example.com",
  "college": "Test University"
}
```

### Mentor Request Payload
```json
{
  "user_input": "How do I implement authentication in my FastAPI app?",
  "context": {
    "team_id": "team_123",
    "project_type": "web_application"
  }
}
```

## Screenshots

Workflow execution screenshots and logs are available in the `screenshots/` directory.