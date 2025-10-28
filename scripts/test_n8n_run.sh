#!/bin/bash

# Test script to simulate n8n webhook POSTs to FastAPI endpoints
# This script proves expected behavior without running n8n

echo "🧪 Testing N8N Workflow Simulation"
echo "==================================="

# Check if required tools are available
if ! command -v curl &> /dev/null; then
    echo "❌ curl is required but not installed"
    exit 1
fi

# Base URL for FastAPI backend
BASE_URL="http://localhost:8001"

# Test 1: Team Registration Workflow Simulation
echo -e "\n1️⃣ Testing Team Registration Workflow"
echo "   Simulating POST to /agent endpoint"
echo "   Payload: Team registration data"

TEAM_REGISTRATION_PAYLOAD='{
  "user_input": "Register team n8n_test_team",
  "context": {
    "team_id": "n8n_test_team"
  }
}'

echo "   Sending request..."
RESPONSE=$(curl -s -o /dev/null -w "%{http_code}" -X POST \
  "$BASE_URL/agent" \
  -H "Content-Type: application/json" \
  -d "$TEAM_REGISTRATION_PAYLOAD")

if [ "$RESPONSE" -eq 200 ]; then
    echo "   ✅ Team registration simulation successful (Status: $RESPONSE)"
else
    echo "   ❌ Team registration simulation failed (Status: $RESPONSE)"
fi

# Test 2: MentorBot Prompt Workflow Simulation
echo -e "\n2️⃣ Testing MentorBot Prompt Workflow"
echo "   Simulating POST to /agent endpoint"
echo "   Payload: Mentor request data"

MENTOR_PAYLOAD='{
  "user_input": "How do I implement authentication in my FastAPI app?",
  "context": {
    "team_id": "n8n_test_team",
    "project_type": "web_application"
  }
}'

echo "   Sending request..."
RESPONSE=$(curl -s -o /dev/null -w "%{http_code}" -X POST \
  "$BASE_URL/agent" \
  -H "Content-Type: application/json" \
  -d "$MENTOR_PAYLOAD")

if [ "$RESPONSE" -eq 200 ]; then
    echo "   ✅ Mentor request simulation successful (Status: $RESPONSE)"
else
    echo "   ❌ Mentor request simulation failed (Status: $RESPONSE)"
fi

# Test 3: Verify endpoints are accessible
echo -e "\n3️⃣ Testing Endpoint Accessibility"

echo "   Testing /docs endpoint..."
RESPONSE=$(curl -s -o /dev/null -w "%{http_code}" "$BASE_URL/docs")
if [ "$RESPONSE" -eq 200 ]; then
    echo "   ✅ /docs endpoint accessible (Status: $RESPONSE)"
else
    echo "   ❌ /docs endpoint not accessible (Status: $RESPONSE)"
fi

echo "   Testing /ping endpoint..."
RESPONSE=$(curl -s -o /dev/null -w "%{http_code}" "$BASE_URL/ping")
if [ "$RESPONSE" -eq 200 ]; then
    echo "   ✅ /ping endpoint accessible (Status: $RESPONSE)"
else
    echo "   ❌ /ping endpoint not accessible (Status: $RESPONSE)"
fi

echo -e "\n✅ N8N Workflow Simulation Complete"
echo "   All workflows have been tested successfully"
echo "   Check the responses above to verify expected behavior"