# CI/CD Deployment To VM

This project now includes a GitHub Actions pipeline that deploys the FastAPI + React app to a VM over SSH using Docker Compose.

## Files Added

- `.github/workflows/deploy-vm.yml`
- `docker-compose.yml`
- `Backend/Dockerfile`
- `frontend/Dockerfile`
- `frontend/nginx.conf`

## VM Requirements

Install these on the VM before first deployment:

```bash
sudo apt update
sudo apt install -y git docker.io docker-compose-plugin
sudo usermod -aG docker $USER
```

Log out and back in after adding your user to the `docker` group.

## GitHub Secrets Required

Add these in GitHub:

`Settings` -> `Secrets and variables` -> `Actions` -> `New repository secret`

Required secrets:

- `VM_HOST`: VM public IP or DNS name.
- `VM_USER`: SSH username on the VM.
- `VM_SSH_KEY`: private SSH key that can access the VM.
- `VM_APP_DIR`: deployment directory on the VM, for example `/opt/fastapi-react-todo`.
- `VM_SSH_PORT`: optional, defaults to `22` if not set.

## How It Works

1. A push to `main` starts GitHub Actions.
2. GitHub builds the Docker Compose stack to catch build errors.
3. GitHub SSHs into the VM.
4. The VM clones the repo if it does not exist yet.
5. The VM resets the app folder to the latest `main` branch.
6. Docker Compose rebuilds and restarts the containers.

## App URLs

Frontend:

```text
http://YOUR_VM_PUBLIC_IP
```

Backend API:

```text
http://YOUR_VM_PUBLIC_IP:4000
```

Backend docs:

```text
http://YOUR_VM_PUBLIC_IP:4000/docs
```

## Manual VM Deploy Command

If you want to deploy manually on the VM:

```bash
cd /opt/fastapi-react-todo
git pull
docker compose up -d --build
```

## Notes

- The backend uses SQLite stored in a Docker volume called `todo-data`.
- The frontend is served by Nginx on port `80`.
- The backend is exposed on port `4000`.
- Open VM firewall/security group ports `22`, `80`, and optionally `4000`.
