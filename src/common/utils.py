import os
import streamlit as st


def get_env(env_name: str) -> str:
    if env_var := os.environ.get(env_name):
        return env_var
    if env_var := st.secrets[env_var]:
        return env_var

    raise Exception(f"Missing setting {env_name}")
