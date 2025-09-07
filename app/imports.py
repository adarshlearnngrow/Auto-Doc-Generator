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
import streamlit as st
# Load variables from .env into process environment (e.g., OPENAI_API_KEY)
# Use find_dotenv so it works even if the CWD is app/ or elsewhere
# Try secrets first, fallback to env
api_key = st.secrets.get("OPENAI_API_KEY", os.getenv("OPENAI_API_KEY"))

if not api_key:
    st.error("No OpenAI API key found. Please set in Streamlit secrets or environment.")
else:
    os.environ["OPENAI_API_KEY"] = api_key  # ensure downstream libs see it
    client = OpenAI(api_key=api_key)