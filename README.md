<div align="center">
  <div align="center">
    <img width="150" height="150" src="public/app-icon.png" alt="Logo" />
  </div>
  <h1 align="center">CompressO-GPU</h1>
  <p align="center">
    <strong>Ultra-Fast Video and Image Compression with NVIDIA GPU Acceleration (NVENC)</strong>
  </p>
  <i align="center">
    A high-performance fork of CompressO supercharged with NVIDIA NVENC & CUDA hardware acceleration.
  </i >
  <br />
  <p align="center">
    Available for <strong>Windows</strong> (NVIDIA GPU accelerated) and cross-platform CPU fallback.
  </p>
  <br />
  <div>
    <a href="https://github.com/codeforreal1/compressO">
      <img alt="Original Project" src="https://img.shields.io/badge/Original%20Project-CompressO-blue?style=flat-square" />
    </a>
    <img alt="NVIDIA NVENC" src="https://img.shields.io/badge/NVIDIA-NVENC%20Accelerated-76B900?style=flat-square&logo=nvidia&logoColor=white" />
    <img alt="License: AGPL-3.0" src="https://img.shields.io/badge/License-AGPL--3.0-orange?style=flat-square" />
  </div>
  <br />
</div>

<div align="center">
  <a href="https://github.com/Fatihx64/CompressO_GPU/releases/download/v3.0.0-gpu/CompressO_3.0.0_x64-setup.exe">
    <img src="https://img.shields.io/badge/Download-Windows_Installer_(.exe)-brightgreen?style=for-the-badge&logo=windows" alt="Download Windows Installer" />
  </a>
  &nbsp;
  <a href="https://github.com/Fatihx64/CompressO_GPU/releases/download/v3.0.0-gpu/CompressO_3.0.0_x64-portable.zip">
    <img src="https://img.shields.io/badge/Download-Portable_Zip_(No_Install)-blue?style=for-the-badge&logo=windows" alt="Download Portable Zip" />
  </a>
  &nbsp;
  <a href="https://github.com/Fatihx64/CompressO_GPU/releases/tag/v3.0.0-gpu">
    <img src="https://img.shields.io/badge/All_Releases-v3.0.0--gpu-orange?style=for-the-badge" alt="All Releases" />
  </a>
</div>

<br />

<div align="center">
  <img src="public/screenshot.png" alt="Screenshot" height="500" style="border-radius: 16px;" />
</div>

---

## 📥 Quick Downloads (Pre-built Binaries)

You do **not** need to clone the repository or install developer tools to use CompressO-GPU. Just download and run:

| Package | Format | Size | Details |
|---|---|---|---|
| **[CompressO_3.0.0_x64-setup.exe](https://github.com/Fatihx64/CompressO_GPU/releases/download/v3.0.0-gpu/CompressO_3.0.0_x64-setup.exe)** | Installer | **~68 MB** | Standard Windows installer with desktop and start menu shortcuts (Recommended) |
| **[CompressO_3.0.0_x64-portable.zip](https://github.com/Fatihx64/CompressO_GPU/releases/download/v3.0.0-gpu/CompressO_3.0.0_x64-portable.zip)** | Portable | **~88 MB** | Standalone portable archive. Extract and run `compressO.exe` directly |

---

## ⚡ What's New in CompressO-GPU?

CompressO-GPU enhances the original [CompressO](https://github.com/codeforreal1/compressO) by bringing native **NVIDIA GPU Hardware Acceleration** to video transcoding:

1. **NVIDIA NVENC Transcoding (10x - 20x Faster)**:
   - **H.264 (NVIDIA GPU ⚡)**: Dedicated `h264_nvenc` hardware encoding.
   - **H.265 / HEVC (NVIDIA GPU ⚡)**: Dedicated `hevc_nvenc` hardware encoding (outstanding compression efficiency at breakthrough speeds).
   - Offloads encoding from the CPU to dedicated silicon on your NVIDIA GeForce GTX/RTX or Quadro card.

2. **Hardware Decoding (CUDA)**:
   - Uses `-hwaccel auto` to decode supported input streams directly on the GPU, eliminating CPU bottlenecks when reading high-resolution or high-bitrate source files.

3. **Smart NVENC Rate Control & Hardware Presets**:
   - Replaces CPU-only `-crf` parameters with NVENC Constant Quality Variable Bitrate (`-rc:v vbr -cq:v <val> -b:v 0`).
   - Automatically maps compression presets:
     - **Thunderbolt**: Low-latency high-speed preset (`-preset p2 -tune ll`).
     - **Ironclad**: High-quality deep-compression preset (`-preset p6 -tune hq`).

4. **Interactive UI GPU Controls**:
   - **GPU Acceleration Switch**: A prominent toggle in the Video Settings tab with real-time detection of your GPU model (e.g., *NVIDIA GeForce RTX 3060*) and live status indicator (**GPU Active** / **CPU Mode**).
   - **Codec Selector**: Explicitly select `H.264 (NVIDIA GPU ⚡)` or `H.265 / HEVC (NVIDIA GPU ⚡)` with container-compatibility checks.
   - Defaults to GPU acceleration enabled whenever an NVIDIA GPU is present.

---

## 📜 Attribution & License

- **Original Project**: This software is based on the fantastic open-source [CompressO](https://github.com/codeforreal1/compressO) project created by **[Code For Real](https://github.com/codeforreal1)**.
- **License**: Both the original project and this fork are distributed under the **[GNU Affero General Public License v3.0 (AGPL-3.0)](LICENSE)**.
- In accordance with the AGPL-3.0 license:
  - All original copyright notices and author attributions are preserved.
  - All modifications for NVIDIA GPU hardware acceleration are documented and open-sourced under the same license terms.

---

## 💻 System Requirements

- **Operating System**: Windows 10 / Windows 11 (64-bit)
- **Graphics Card**: NVIDIA GeForce GTX 900+ / 10 / 16 / RTX 20 / 30 / 40 / 50 series or NVIDIA Quadro/RTX workstation GPUs
- **Driver**: Modern NVIDIA Display Driver (Game Ready or Studio Driver) with NVENC support
- **CPU Fallback**: Full CPU compression fallback (`libx264`, `libx265`, `libvpx-vp9`) is maintained for systems without a dedicated NVIDIA GPU.

---

## 🚀 Quick Start & Running

### Option 1: Quick Launcher (Pre-built)
Double-click [`run-compressO-gpu.bat`](run-compressO-gpu.bat) in the project directory to launch CompressO with GPU acceleration immediately.

### Option 2: Run via Terminal
```powershell
# Run the compiled debug executable:
.\src-tauri\target\debug\compressO.exe

# Or start in development mode:
npx pnpm tauri dev
```

---

## 🛠️ Building from Source

### Prerequisites
1. **Node.js** (v18 or newer)
2. **Rust** toolchain:
   ```powershell
   winget install Rustlang.Rustup
   rustup default stable
   ```
3. **pnpm**:
   ```powershell
   npm install -g pnpm
   ```

### Build Steps
1. Install frontend dependencies:
   ```powershell
   pnpm install
   ```
2. Build frontend and application bundle:
   ```powershell
   # Development mode:
   pnpm tauri dev

   # Production installer / executable:
   pnpm tauri build
   ```

---

## 🖼️ Screenshots

<details>
<summary><strong>View Screenshots</strong></summary>

<img src="https://github.com/user-attachments/assets/f89d3c18-20fd-4359-937b-d4f0c2a4a3f8" width="100%" alt="Compression Output" loading="lazy" />
<img src="https://github.com/user-attachments/assets/49f95db6-5e9e-4abf-bc7f-54dd3f0ae534" width="100%" alt="Trim/Split feature" loading="lazy" />
<img src="https://github.com/user-attachments/assets/b96fcd4b-1d02-4394-9dd7-419cb4568234" width="100%" alt="Batch Compression" loading="lazy" />
<img src="https://github.com/user-attachments/assets/d86dae45-60c9-4d54-b7b2-98674105103a" width="576" alt="Video/Audio Config" loading="lazy" />
<img src="https://github.com/user-attachments/assets/f7877316-ab91-4f08-9b4d-e2bb21cc8d5a" width="576" alt="App Settings" loading="lazy" />

</details>

---

## 🤝 Contributing

Contributions, bug reports, and suggestions are welcome! Please open an issue or pull request on GitHub.
