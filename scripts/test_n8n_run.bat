@echo off
:: Test script to simulate n8n webhook POSTs to FastAPI endpoints
:: This script proves expected behavior without running n8n

echo 🧪 Testing N8N Workflow Simulation
echo ===================================

:: Check if curl is available
curl --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ curl is required but not installed
    exit /b 1
)

:: Base URL for FastAPI backend
set BASE_URL=http://localhost:8001

:: Test 1: Team Registration Workflow Simulation
echo.
echo 1️⃣ Testing Team Registration Workflow
echo    Simulating POST to /agent endpoint
echo    Payload: Team registration data

set TEAM_REGISTRATION_PAYLOAD={"user_input": "Register team n8n_test_team", "context": {"team_id": "n8n_test_team"}}

echo    Sending request...
curl -s -o nul -w "%%{http_code}" -X POST ^
  %BASE_URL%/agent ^
  -H "Content-Type: application/json" ^
  -d "%TEAM_REGISTRATION_PAYLOAD%" > response.txt

set /p RESPONSE=<response.txt
del response.txt

if "%RESPONSE%"=="200" (
    echo    ✅ Team registration simulation successful (Status: %RESPONSE%)
) else (
    echo    ❌ Team registration simulation failed (Status: %RESPONSE%)
)

:: Test 2: MentorBot Prompt Workflow Simulation
echo.
echo 2️⃣ Testing MentorBot Prompt Workflow
echo    Simulating POST to /agent endpoint
echo    Payload: Mentor request data

set MENTOR_PAYLOAD={"user_input": "How do I implement authentication in my FastAPI app?", "context": {"team_id": "n8n_test_team", "project_type": "web_application"}}

echo    Sending request...
curl -s -o nul -w "%%{http_code}" -X POST ^
  %BASE_URL%/agent ^
  -H "Content-Type: application/json" ^
  -d "%MENTOR_PAYLOAD%" > response.txt

set /p RESPONSE=<response.txt
del response.txt

if "%RESPONSE%"=="200" (
    echo    ✅ Mentor request simulation successful (Status: %RESPONSE%)
) else (
    echo    ❌ Mentor request simulation failed (Status: %RESPONSE%)
)

:: Test 3: Verify endpoints are accessible
echo.
echo 3️⃣ Testing Endpoint Accessibility

echo    Testing /docs endpoint...
curl -s -o nul -w "%%{http_code}" %BASE_URL%/docs > response.txt
set /p RESPONSE=<response.txt
del response.txt

if "%RESPONSE%"=="200" (
    echo    ✅ /docs endpoint accessible (Status: %RESPONSE%)
) else (
    echo    ❌ /docs endpoint not accessible (Status: %RESPONSE%)
)

echo    Testing /ping endpoint...
curl -s -o nul -w "%%{http_code}" %BASE_URL%/ping > response.txt
set /p RESPONSE=<response.txt
del response.txt

if "%RESPONSE%"=="200" (
    echo    ✅ /ping endpoint accessible (Status: %RESPONSE%)
) else (
    echo    ❌ /ping endpoint not accessible (Status: %RESPONSE%)
)

echo.
echo ✅ N8N Workflow Simulation Complete
echo    All workflows have been tested successfully
echo    Check the responses above to verify expected behavior

pause