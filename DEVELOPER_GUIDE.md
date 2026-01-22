# Developer Guide

## Project Structure
- `app.py`: Main Streamlit app, handles authentication, navigation, and page routing.
- `predict_page.py`: Handles medicine quantity prediction logic and UI.
- `explore_page.py`: Data exploration and visualization page.
- `records.py`: Displays and manages medicine records.
- `add_medicine_page.py`: UI and logic for adding new medicine records.
- `add_user_page.py`: UI and logic for adding new users.
- `improvement.py`: Additional prediction/analysis utilities.
- `model_saved/` and `Model/`: Contains trained model files and feature columns.
- `Historical_Data_7_Aug_2024.csv`: Main dataset for predictions and exploration.
- `requirements.txt`: Python dependencies.
- `.gitignore`: Git ignore rules.
- `README.md`, `DEPLOYMENT.md`: User and deployment documentation.

## Key Concepts
- **Authentication**: User login is handled in `app.py` using a SQLite database (`users.db`). Passwords are hashed with bcrypt.
- **Database**: Medicine records are stored in `Historical_Data_Medicine.db`. Tables are created if missing.
- **Prediction**: Models are loaded from `Model/` and used for predictions in `predict_page.py` and `improvement.py`.
- **Data Loading**: All data files must be present in the root or referenced folders and not ignored by `.gitignore`.
- **Session State**: Streamlit's `st.session_state` is used for user state and navigation.

## Adding New Features
- Add new pages by creating a new Python file and importing its main function in `app.py`.
- Use Streamlit widgets for UI and `st.session_state` for navigation.
- For new models, save them in `Model/` and update the relevant page to load and use them.

## Deployment Notes
- All required files (models, datasets, assets) must be tracked by git and present in the repo.
- Update `.gitignore` to allow new data files if needed.
- For Streamlit Cloud, push to GitHub and redeploy.

## Troubleshooting
- FileNotFoundError: Ensure the file is in the repo and not ignored.
- Database errors: Check that tables are created at app startup.
- Dependency errors: Update `requirements.txt` and redeploy.

## Contact
For questions or contributions, open an issue or pull request on the GitHub repository.
