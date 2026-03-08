#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Manual deployment to HuggingFace Spaces using Hub API."""
import os
import sys
from pathlib import Path
from huggingface_hub import HfApi, create_repo

def deploy_to_spaces():
    """Deploy the environment to HuggingFace Spaces manually."""

    # Configuration
    repo_id = "mo35/code-refactor-gym"
    repo_type = "space"
    space_sdk = "docker"

    print(f">> Deploying to HuggingFace Spaces: {repo_id}")

    # Initialize HF API
    api = HfApi()

    # Get current user
    try:
        user = api.whoami()
        print(f"[OK] Authenticated as: {user['name']}")
    except Exception as e:
        print(f"[ERROR] Authentication failed: {e}")
        return False

    # Create repository
    try:
        print(f"\n>> Creating Space repository...")
        repo_url = create_repo(
            repo_id=repo_id,
            repo_type=repo_type,
            space_sdk=space_sdk,
            exist_ok=True,
            private=False,
        )
        print(f"[OK] Repository created/exists: {repo_url}")
    except Exception as e:
        print(f"[ERROR] Failed to create repository: {e}")
        return False

    # Prepare files to upload
    env_dir = Path(r"D:\Northflank + openv\code_refactor_gym")

    # Move Dockerfile to root for Spaces
    dockerfile_src = env_dir / "server" / "Dockerfile"
    dockerfile_dst = env_dir / "Dockerfile"

    if dockerfile_src.exists() and not dockerfile_dst.exists():
        import shutil
        shutil.copy(dockerfile_src, dockerfile_dst)
        print(f"[OK] Copied Dockerfile to root")

    # Create .spacesconfig for Docker Space
    spacesconfig = env_dir / ".spacesconfig"
    spacesconfig.write_text("sdk: docker\nsdk_version: latest\n", encoding="utf-8")
    print(f"[OK] Created .spacesconfig")

    # Upload files
    try:
        print(f"\n>> Uploading files to Space...")

        # Upload key files one by one to avoid encoding issues
        files_to_upload = [
            "Dockerfile",
            ".spacesconfig",
            "openenv.yaml",
            "pyproject.toml",
            "models.py",
            "__init__.py",
            "README.md",
        ]

        for filename in files_to_upload:
            file_path = env_dir / filename
            if file_path.exists():
                try:
                    api.upload_file(
                        path_or_fileobj=str(file_path),
                        path_in_repo=filename,
                        repo_id=repo_id,
                        repo_type=repo_type,
                    )
                    print(f"  [OK] Uploaded {filename}")
                except Exception as e:
                    print(f"  [WARN] Warning uploading {filename}: {e}")

        # Upload server directory
        server_files = ["app.py", "code_refactor_gym_environment.py", "__init__.py"]
        for filename in server_files:
            file_path = env_dir / "server" / filename
            if file_path.exists():
                try:
                    api.upload_file(
                        path_or_fileobj=str(file_path),
                        path_in_repo=f"server/{filename}",
                        repo_id=repo_id,
                        repo_type=repo_type,
                    )
                    print(f"  [OK] Uploaded server/{filename}")
                except Exception as e:
                    print(f"  [WARN] Warning uploading server/{filename}: {e}")

        print(f"\n[SUCCESS] Deployment complete!")
        print(f"Space URL: https://huggingface.co/spaces/{repo_id}")
        print(f"API URL: https://{repo_id.replace('/', '-')}.hf.space")

        return True

    except Exception as e:
        print(f"[ERROR] Failed to upload files: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = deploy_to_spaces()
    sys.exit(0 if success else 1)
