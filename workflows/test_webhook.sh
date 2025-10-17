#!/bin/bash

echo "Testing N8N Hackathon Registration Workflow"
echo "========================================"
echo ""

echo "Sending registration for Team Alpha..."
curl -X POST http://localhost:5678/webhook/team-registered \
  -H "Content-Type: application/json" \
  -d '{"team_name": "Team Alpha", "members": ["Alice", "Bob"], "email": "alpha@example.com", "college": "XYZ University"}'

echo ""
echo "Sending registration for Team Beta..."
curl -X POST http://localhost:5678/webhook/team-registered \
  -H "Content-Type: application/json" \
  -d '{"team_name": "Team Beta", "members": ["Charlie", "David"], "email": "beta@example.com", "college": "ABC University"}'

echo ""
echo "Sending registration for Team Gamma..."
curl -X POST http://localhost:5678/webhook/team-registered \
  -H "Content-Type: application/json" \
  -d '{"team_name": "Team Gamma", "members": ["Eve", "Frank"], "email": "gamma@example.com", "college": "DEF University"}'

echo ""
echo ""
echo "🎉 All team registrations sent!"
echo "Check your N8N interface and email for results."