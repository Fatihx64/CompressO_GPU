import os
import sys
import json
import urllib.request
import urllib.parse
import subprocess

def get_github_token():
    res = subprocess.run(['git', 'credential', 'fill'], input=b'protocol=https\nhost=github.com\n\n', capture_output=True)
    for line in res.stdout.decode().splitlines():
        if line.startswith('password='):
            return line.split('=', 1)[1]
    return None

def main():
    token = get_github_token()
    if not token:
        print("ERROR: Could not retrieve GitHub token from git credential manager.")
        sys.exit(1)

    repo = "Fatihx64/CompressO_GPU"
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json",
        "User-Agent": "CompressO-Release-Uploader"
    }

    # Check if release with tag already exists
    tag = "v3.0.0-gpu"
    print(f"Checking existing release for tag {tag}...")
    req = urllib.request.Request(f"https://api.github.com/repos/{repo}/releases/tags/{tag}", headers=headers)
    release = None
    try:
        with urllib.request.urlopen(req) as resp:
            release = json.loads(resp.read().decode())
            print(f"Found existing release ID {release['id']}")
    except urllib.error.HTTPError as e:
        if e.code == 404:
            print("Release does not exist yet. Creating new release...")
        else:
            raise

    body_text = """## ⚡ CompressO GPU v3.0.0 — NVIDIA NVENC Hardware Acceleration

CompressO-GPU brings native NVIDIA GPU hardware acceleration (NVENC & CUDA) to [CompressO](https://github.com/codeforreal1/compressO), enabling **8x to 15x faster** video compression with dramatically reduced CPU usage.

---

### 🚀 Key Features & Improvements
- **NVIDIA NVENC Hardware Encoding:** Full support for `H.264 (NVENC)` and `HEVC / H.265 (NVENC)`.
- **Hardware-Accelerated Decoding:** Automatically decodes video streams on your NVIDIA GPU (`-hwaccel auto`).
- **Optimized Rate Control:** Calibrated Variable Bitrate Constant Quality (`-rc:v vbr -cq:v <val> -b:v 0`) specifically engineered for NVENC so video quality remains sharp and artifacts are prevented.
- **Dynamic Hardware Detection:** Automatically probes and detects connected NVIDIA GPU model (e.g. RTX 3060, RTX 4070, GTX 1660) and displays active GPU status in the UI.
- **CPU Fallback:** Seamless toggle to switch back to traditional CPU compression (`libx264`, `libx265`) whenever desired.
- **Zero bloatware:** Clean standalone binaries, ready to run without dev dependencies.

---

### 📦 Downloads & Binaries

| Asset | Description | Size | Recommended For |
|---|---|---|---|
| 💾 **[CompressO_3.0.0_x64-setup.exe](https://github.com/Fatihx64/CompressO_GPU/releases/download/v3.0.0-gpu/CompressO_3.0.0_x64-setup.exe)** | **Windows Installer (NSIS)** | **~68 MB** | **All Windows users (Recommended)** |
| 📦 **[CompressO_3.0.0_x64-portable.zip](https://github.com/Fatihx64/CompressO_GPU/releases/download/v3.0.0-gpu/CompressO_3.0.0_x64-portable.zip)** | **Portable ZIP (No installation)** | **~88 MB** | **Extract & Run anywhere** |

---

### 💻 System Requirements
- **OS:** Windows 10 or Windows 11 (64-bit)
- **GPU:** NVIDIA GeForce, RTX, GTX, or Quadro GPU supporting NVENC
- **NVIDIA Drivers:** Version 522.25 or newer recommended

---
*Upstream original project by [Code For Real](https://github.com/codeforreal1/compressO) licensed under GNU AGPL-3.0.*
"""

    if not release:
        payload = {
            "tag_name": tag,
            "target_commitish": "main",
            "name": "CompressO GPU v3.0.0 (NVIDIA NVENC/CUDA)",
            "body": body_text,
            "draft": False,
            "prerelease": False
        }
        create_req = urllib.request.Request(
            f"https://api.github.com/repos/{repo}/releases",
            data=json.dumps(payload).encode('utf-8'),
            headers=headers,
            method="POST"
        )
        with urllib.request.urlopen(create_req) as resp:
            release = json.loads(resp.read().decode())
            print(f"Created release with ID {release['id']}: {release['html_url']}")

    # Get upload URL
    upload_url_template = release["upload_url"].split("{")[0]

    # Files to upload
    files_to_upload = [
        ("CompressO_3.0.0_x64-setup.exe", "dist-release/CompressO_3.0.0_x64-setup.exe", "application/octet-stream"),
        ("CompressO_3.0.0_x64-portable.zip", "dist-release/CompressO_3.0.0_x64-portable.zip", "application/zip")
    ]

    # Check existing assets to delete them if re-uploading
    existing_assets = {a["name"]: a["id"] for a in release.get("assets", [])}

    for file_name, file_path, content_type in files_to_upload:
        if file_name in existing_assets:
            asset_id = existing_assets[file_name]
            print(f"Deleting older asset '{file_name}' (ID {asset_id})...")
            del_req = urllib.request.Request(
                f"https://api.github.com/repos/{repo}/releases/assets/{asset_id}",
                headers=headers,
                method="DELETE"
            )
            with urllib.request.urlopen(del_req) as resp:
                print(f"Old asset deleted.")

        print(f"Uploading {file_name} ({os.path.getsize(file_path):,} bytes)...")
        with open(file_path, "rb") as f:
            data = f.read()

        params = urllib.parse.urlencode({"name": file_name})
        upload_req = urllib.request.Request(
            f"{upload_url_template}?{params}",
            data=data,
            headers={
                "Authorization": f"token {token}",
                "Content-Type": content_type,
                "User-Agent": "CompressO-Release-Uploader"
            },
            method="POST"
        )
        with urllib.request.urlopen(upload_req) as resp:
            uploaded_asset = json.loads(resp.read().decode())
            print(f"Successfully uploaded {file_name}! Download URL: {uploaded_asset['browser_download_url']}")

    print("\nALL ASSETS UPLOADED SUCCESSFULLY!")
    print(f"Release URL: {release['html_url']}")

if __name__ == "__main__":
    main()
