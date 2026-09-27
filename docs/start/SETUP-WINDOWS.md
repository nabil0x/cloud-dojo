# Setup on Windows (WSL2 path — the only sane one)

Do everything inside Ubuntu on WSL2. Docker Desktop is just the engine behind it.

## 1. Enable WSL2 + install Ubuntu
```powershell
wsl --install -d Ubuntu
```
Reboot if asked. Open the **Ubuntu** app (not PowerShell) for everything below.

## 2. Install Docker Desktop
1. Download Docker Desktop for Windows, install with **WSL2 backend** enabled.
2. Settings → Resources → WSL integration → enable **Ubuntu**.
3. Back in Ubuntu: `docker run hello-world` must print `Hello from Docker!` **without `sudo`**.

## 3. Course tooling
```bash
sudo apt update && sudo apt install -y curl python3 unzip
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o awscliv2.zip \
  && unzip -q awscliv2.zip && sudo ./aws/install && aws --version
```

## Pitfalls (Windows-specific)
- **Running everything in PowerShell** instead of Ubuntu: paths, line endings, and socket mounts all misbehave. Ubuntu terminal, always.
- **Files in `/mnt/c` are slow**: keep the repo inside WSL (`~/cloud-dojo`, clone fresh there), not on the Windows drive.
- **`localhost:4566` unreachable**: usually Docker Desktop's WSL integration toggled off for Ubuntu. Re-check Settings.
- **VPN/firewall blocks pulls**: corporate Zscaler-style proxies break the emulator image pull; tether or allowlist `docker.io`.
- **Old machine without virtualization**: enable VT-x/AMD-V in BIOS, or use the Codespaces button instead (zero install).
