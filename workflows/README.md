# Hackathon Registration Workflow for N8N

This document provides step-by-step instructions for setting up and using the N8N workflow for automating hackathon team registration.

## Prerequisites

1. Node.js and npm installed on your system
2. N8N installed globally (`npm install -g n8n`)
3. The FastAPI backend running on your local machine
4. SMTP credentials for sending emails (e.g., Gmail App Password)

## Starting N8N

1. Open a terminal in your project directory
2. Run the following command:
   ```bash
   n8n
   ```
3. Wait for N8N to start completely. You should see a message like:
   ```
   Editor is now accessible via: http://localhost:5678
   ```
4. Open your browser and navigate to http://localhost:5678

## Importing the Workflow

1. In the N8N interface, click the "Import" button in the top-right corner
2. Choose "Import from Clipboard"
3. Copy the entire content of the `hackathon_registration_workflow.json` file
4. Paste it into the clipboard import area
5. Click "Import"
6. You should now see 6 nodes connected in sequence:
   - Start
   - Webhook
   - Register Team
   - Store in BHIV Bucket
   - Email Judges
   - Run Agent Evaluation

## Configuring the Workflow

### Setting Backend URLs

1. Click the "Register Team" node
2. In the Parameters section, set the URL to:
   ```
   http://localhost:8002/register
   ```
   (Use your deployed backend URL when you go live)

3. Click the "Run Agent Evaluation" node
4. Set its URL to:
   ```
   http://localhost:8002/agent
   ```

5. Click the "Store in BHIV Bucket" node
6. Replace the placeholder URL with your actual storage service endpoint
   (You can mock this for now by using a service like https://httpbin.org/post for testing)

### Configuring the Email Node

1. Click on the "Email Judges" node
2. In the parameters, set:
   - To: [judges@example.com](mailto:judges@example.com) (replace with actual judge emails)
   - Subject: New Team Registered
   - Text: A new team has registered: {{ $json.team_name }}

3. Under Credentials, click "Add New" and select "SMTP"
4. Enter your SMTP settings:
   - Host: smtp.gmail.com (for Gmail)
   - Port: 587
   - User: your_email@gmail.com
   - Password: your Gmail App Password (not your main password)
   - TLS: true

5. Click "Save"

Note: To generate a Gmail App Password:
1. Go to https://myaccount.google.com/apppasswords
2. Sign in to your Google Account
3. Generate a new app password for "N8N"
4. Use this password in the SMTP configuration

## Testing the Workflow

1. Click the "Webhook" node
2. Copy the Webhook URL shown in the right panel
   It will look like:
   ```
   http://localhost:5678/webhook/team-registered
   ```

3. Open Postman or use curl to send a POST request to this URL with the following JSON payload:
   ```json
   {
     "team_name": "Team Alpha",
     "members": ["Alice", "Bob"],
     "email": "team@example.com",
     "college": "XYZ University"
   }
   ```

4. Watch N8N's interface:
   - Each node should turn green if it runs successfully
   - Check your FastAPI logs to confirm a hit on the /register endpoint
   - Check your email to confirm the notification was sent

## Activating the Workflow

1. Once everything works correctly, click "Save" in the top-right corner
2. Click "Activate Workflow"
3. You'll see a green toggle indicating your automation is live

## How It Works

With the workflow activated, any new team that POSTs to the webhook URL will automatically:
1. Register in your FastAPI backend
2. Store registration data in the BHIV Bucket
3. Send an email notification to the judges
4. Trigger an agent evaluation

## Troubleshooting

- If nodes fail, check the error messages in the node details
- Ensure your FastAPI backend is running on the correct port
- Verify all URLs are correctly configured
- Check that your SMTP credentials are correct
- Make sure your firewall allows connections to the required services

## Customization

You can customize this workflow by:
- Adding more nodes for additional processing steps
- Modifying the email template
- Adding conditions based on team information
- Integrating with other services like Slack or Discord for notifications