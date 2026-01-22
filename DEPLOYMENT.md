# Deployment & Hosting Guide

## Local Deployment
1. Ensure Python 3.12+ is installed.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the app:
   ```bash
   streamlit run app.py
   ```

## Cloud Hosting (Streamlit Cloud)
1. Push your code to GitHub (public or private repo).
2. Go to [Streamlit Cloud](https://streamlit.io/cloud) and connect your repo.
3. Set up secrets/environment variables if needed.
4. App will auto-deploy and update on new commits.

## Heroku Deployment
1. Add a `Procfile` with:
   ```
   web: streamlit run app.py
   ```
2. Add `requirements.txt` and (optionally) `setup.sh` for build steps.
3. Push to Heroku and deploy.

## General Tips
- Use relative paths for assets and databases.
- Remove sensitive files before hosting.
- Configure `.streamlit/config.toml` for custom ports and headless mode.

## Troubleshooting
- Check logs for errors (Streamlit, Heroku, etc.).
- Ensure all required files are present in the repo.
- For database issues, verify file paths and permissions.
