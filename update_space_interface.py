#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Update Space with web interface."""
from pathlib import Path
from huggingface_hub import HfApi

def update_interface():
    api = HfApi()
    repo_id = "mo35/code-refactor-gym"
    repo_type = "space"

    print("Uploading web interface to Space...")

    # Upload the interface file
    env_dir = Path(r"D:\Northflank + openv\code_refactor_gym")
    interface_file = env_dir / "app_interface.py"

    if interface_file.exists():
        api.upload_file(
            path_or_fileobj=str(interface_file),
            path_in_repo="app_interface.py",
            repo_id=repo_id,
            repo_type=repo_type,
        )
        print("[OK] Uploaded app_interface.py")
    else:
        print("[ERROR] app_interface.py not found")
        return False

    print("\n[SUCCESS] Interface uploaded!")
    print("The Space will rebuild automatically.")
    print("Visit: https://huggingface.co/spaces/mo35/code-refactor-gym")

    return True

if __name__ == "__main__":
    update_interface()
