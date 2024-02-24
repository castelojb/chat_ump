import os


def get_env(env_name: str) -> str:
    if env_var := os.environ.get(env_name):
        return env_var

    raise Exception(f"Missing database setting {env_name}")
