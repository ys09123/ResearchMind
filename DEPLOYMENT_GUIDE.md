# ResearchMind Deployment Guide

## Streamlit Cloud Setup

### Issue: `groq.NotFoundError`

If you see this error after deploying to Streamlit Cloud, it means the Groq API key is missing or invalid.

### Quick Fix

1. **Get your Groq API Key**
   - Go to https://console.groq.com
   - Sign up or log in
   - Navigate to **API Keys**
   - Create a new key and copy it

2. **Add to Streamlit Cloud**
   - Open your deployed app
   - Click the **☰ menu** (top right)
   - Select **Manage app**
   - Click **Secrets** in the left sidebar
   - Add this line:
     ```
     GROQ_API_KEY = your_actual_api_key_here
     ```
   - Click **Save**
   - Your app will automatically redeploy

3. **Test your app**
   - Refresh the page
   - Enter a research topic
   - Click "Run Pipeline"

### Local Development

To test locally before deploying:

1. **Create `.streamlit/secrets.toml`** in your project root:
   ```toml
   GROQ_API_KEY = "your_groq_api_key"
   ```

2. **Run the app:**
   ```bash
   streamlit run app.py
   ```

### Troubleshooting

**Problem: "Missing GROQ_API_KEY" error**
- Check that your API key is correctly added to Streamlit Cloud secrets
- Ensure no extra spaces or quotes around the key value

**Problem: "Groq Model Not Found"**
- Your account may not have access to the configured models
- Check available models: https://console.groq.com/docs/models
- Edit `agents.py` to use available models (e.g., `mixtral-8x7b-32768`, `gemma2-9b-it`)

**Problem: "Authentication Failed" / "401 Unauthorized"**
- Your API key is expired or invalid
- Generate a new key from https://console.groq.com/keys
- Update the secret in Streamlit Cloud

### Available Groq Models

The app automatically falls back to alternative models if the primary ones aren't available:

| Primary | Fallback |
|---------|----------|
| `llama-3.3-70b-versatile` | `mixtral-8x7b-32768` |
| `llama-3.1-8b-instant` | `gemma2-9b-it` |

You can modify these in `agents.py` lines 16-25.

### Environment Variables

The app looks for the `GROQ_API_KEY` environment variable from:
1. `.streamlit/secrets.toml` (local)
2. Streamlit Cloud Secrets (production)
3. System environment variables

### GitHub Repository Link

When deploying from GitHub, make sure:
- You've committed all code changes
- Your repo is public (or you have access)
- Streamlit Cloud has permission to access your repo
