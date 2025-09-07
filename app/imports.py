# Standard library
import ast
import hashlib
import json
import os
import shutil
import stat
import sys
import tempfile
from dataclasses import dataclass
from itertools import chain
from pathlib import Path
from typing import List, Literal, TypedDict

# Third-party
import nbformat
import pandas as pd
from docx import Document as DocxDocument
from git import Repo, GitCommandError
from openai import OpenAI
from langgraph.graph import StateGraph, END
from langchain_core.documents import Document
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from dotenv import load_dotenv, find_dotenv
# Standard library
import os
from dotenv import load_dotenv, find_dotenv

# --- Resolve OPENAI creds: prefer Streamlit secrets (Cloud), else .env/env (local) ---
def resolve_openai_key() -> str | None:
    # 1) Try Streamlit secrets (if Streamlit is installed & secrets exist)
    try:
        import streamlit as st  # noqa: F401
        try:
            # only touch st.secrets if it's configured
            if "OPENAI_API_KEY" in st.secrets:
                return st.secrets["OPENAI_API_KEY"]
        except Exception:
            # secrets.toml not present locally → ignore
            pass
    except Exception:
        # streamlit not installed / not running
        pass

    # 2) Fall back to .env / environment
    _env_path = find_dotenv(usecwd=True)
    if _env_path:
        load_dotenv(_env_path)
    return os.getenv("OPENAI_API_KEY")

# --- Use it ---
OPENAI_API_KEY = resolve_openai_key()

if not OPENAI_API_KEY:
    # If you are inside Streamlit, you can show a UI error; otherwise raise.
    try:
        import streamlit as st
        #st.error("❌ No OpenAI API key found. Add it to Streamlit secrets or your local .env.")
    except Exception:
        raise RuntimeError("No OPENAI_API_KEY found in Streamlit secrets or environment (.env).")
else:
    os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY  # so LangChain etc. can see it
    client = OpenAI(api_key=OPENAI_API_KEY)
