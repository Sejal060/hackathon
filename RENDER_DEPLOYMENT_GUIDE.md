# Render Deployment Guide for HackaAIverse

This guide provides instructions for deploying the HackaAIverse application to Render.com.

## Prerequisites

- A Render.com account
- Your code pushed to a Git repository (GitHub, GitLab, etc.)

## Deployment Steps

### 1. Fix Common Issues Before Deployment

- **Method Name Consistency**: Ensure method names match between imports and implementations
  - Example: In `src/main.py`, we call `reasoning.plan()`, so the method in `ReasoningModule` must be named `plan()` not `plan_action()`

- **Package Versions**: Use compatible package versions
  - NumPy: Use `numpy>=1.20.0` instead of `numpy>=2.0.0` for better compatibility
  - Avoid using beta or alpha versions of packages in production

- **Environment Variables**: Ensure all required environment variables are set in Render
  - GROQ_API_KEY (required for AI functionality)
  - Other API keys as needed

### 2. Deploy to Render

1. Log in to your Render dashboard
2. Click "New" and select "Web Service"
3. Connect your Git repository
4. Configure your service:
   - **Name**: ai-agent (or your preferred name)
   - **Environment**: Python
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn src.main:app --host 0.0.0.0 --port $PORT`

5. Add environment variables:
   - Click "Advanced" > "Add Environment Variable"
   - Add your GROQ_API_KEY and any other required variables

6. Click "Create Web Service"

### 3. Verify Deployment

1. Wait for the build and deployment to complete
2. Visit your service URL (e.g., https://ai-agent.onrender.com)
3. Check the API documentation at /docs endpoint
4. Test the /ping endpoint to verify basic functionality

### 4. Troubleshooting

If you encounter errors:

1. Check Render logs for specific error messages
2. Verify all environment variables are set correctly
3. Ensure package versions are compatible with Render's environment
4. Check for method name mismatches or import errors

### 5. Updating Your Deployment

Render automatically deploys new commits to your connected repository. To update:

1. Make changes to your code locally
2. Commit and push to your repository
3. Render will automatically rebuild and deploy

## Additional Resources

- [Render Python Documentation](https://render.com/docs/deploy-python)
- [FastAPI Deployment Guide](https://fastapi.tiangolo.com/deployment/)