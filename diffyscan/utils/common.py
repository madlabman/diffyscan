import json
import os
import sys
from urllib.parse import urlparse

import requests

from .logger import logger
from .types import Config


def load_env(variable_name, required=True, masked=False):
    value = os.getenv(variable_name, default=None)

    if required and not value:
        logger.error("Env not found", variable_name)
        sys.exit(1)

    printable_value = mask_text(value) if masked and value is not None else str(value)

    if printable_value:
        logger.okay(f"{variable_name}", printable_value)
    else:
        logger.info(f"{variable_name} var is not set")

    return value


def load_config(path: str) -> Config:
    with open(path, mode="r") as config_file:
        return json.load(config_file)


def fetch(url, headers={}):
    logger.log(f"Fetch: {url}")
    response = requests.get(url, headers=headers)

    if response.status_code == 404:
        return None

    if not response.ok and response.status_code != 200:
        logger.error("Request failed", url)
        logger.error("Status", response.status_code)
        logger.error("Response", response.text)

    return response.json()


def mask_text(text, mask_start=3, mask_end=3):
    text_length = len(text)
    mask = "*" * (text_length - mask_start - mask_end)
    return text[:mask_start] + mask + text[text_length - mask_end :]


def parse_repo_link(repo_link):
    parse_result = urlparse(repo_link)
    repo_location = [item.strip("/") for item in parse_result[2].split("tree")]
    user_slash_repo = repo_location[0]
    return user_slash_repo
