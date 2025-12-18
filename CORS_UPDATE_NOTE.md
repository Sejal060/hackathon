# CORS Configuration Update

Updated CORS middleware in src/main.py to explicitly allow:
- http://localhost:3000 (for local development)
- https://<yash-frontend-url> (placeholder for Yash's frontend URL)

This change ensures frontend safety and proper cross-origin resource sharing between the frontend and backend services.

The specific configuration:
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "https://<yash-frontend-url>"  # Replace with actual frontend URL
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

Next steps:
1. Replace "https://<yash-frontend-url>" with the actual frontend deployment URL
2. Test CORS functionality with frontend integration