Based upon the following Youtube tutorial: https://www.youtube.com/watch?v=XZdY15sHUa8

Projects uses UV for installing any dependencies.
https://docs.astral.sh/uv/getting-started/installation/#standalone-installer

Projects uses Streamlit for building a UI.

How to initialize a new UV project?
uv init .

How to add dependencies?
uv add streamlit anthropic PyPDF2 python-dotenv

How to run the streamlit application?
uv run streamlit run main.py
