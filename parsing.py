import os
import sys
from pathlib import Path

import yaml


def parse_configuration():
    path = Path.cwd() / "labels.yml"
    contents = path.read_text("utf-8")
    parsed: dict[str, dict] = yaml.safe_load(contents)

    owners = {}
    updates = {}
    labels = {}

    for operation, data in parsed.items():
        for value in data:
            if operation == "owners":
                owner = str(value.get("name", ""))
                is_org = bool(value.get("is_org", True))
                token = str(value.get("token", ""))

                if len(token) == 0:
                    sys.exit(f"Token of owner {owner} is empty!")

                owners[owner] = {
                    "is_org": is_org,
                    "token": str(os.environ.get(token, ""))
                }
            elif operation == "updates":
                current = str(value.get("current", ""))
                target = str(value.get("target", ""))
                delete = bool(value.get("delete", False))

                updates[current] = {
                    "current": current,
                    "target": target,
                    "delete": delete
                }
            elif operation == "custom":
                name = str(value.get("name", ""))
                description = str(value.get("description", ""))
                color = str(value.get("color", "ffffff")).lower()

                labels[name] = {
                    "name": name,
                    "description": description,
                    "color": color
                }

    return owners, updates, labels
