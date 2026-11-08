"""Entry point for Streamlit Community Cloud: runs the Ops morning board in dashboard/app.py."""
import runpy
from pathlib import Path

runpy.run_path(str(Path(__file__).resolve().parent / "dashboard" / "app.py"), run_name="__main__")
