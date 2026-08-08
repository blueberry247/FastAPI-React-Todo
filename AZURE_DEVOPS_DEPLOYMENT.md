# Azure DevOps CI/CD

This project includes `azure-pipelines.yml` for deploying the FastAPI + React Docker Compose app to a VM.

## What The Pipeline Does

1. Runs when you push to `main`.
2. Builds the Docker Compose stack on an Azure DevOps hosted agent.
3. Copies the project files to your VM over SSH.
4. Runs `docker compose up -d --build` on the VM.

## VM Requirements

Run this once on the VM:

```bash
sudo apt update
sudo apt install -y docker.io docker-compose-plugin
sudo usermod -aG docker $USER
```

Then log out and back in so Docker group permissions apply.

## Azure DevOps Setup

1. Push this repo to Azure Repos or connect the GitHub repo to Azure DevOps.
2. In Azure DevOps, go to `Project settings`.
3. Go to `Service connections`.
4. Create a new `SSH` service connection.
5. Name it exactly:

```text
fastapi-vm-ssh
```

6. Add your VM details:

- Host name: your VM public IP or DNS name
- Port: `22`
- Username: your VM SSH username
- Private key: your SSH private key

7. Go to `Pipelines` -> `New pipeline`.
8. Select your repository.
9. Choose `Existing Azure Pipelines YAML file`.
10. Select:

```text
azure-pipelines.yml
```

## Change The VM Deploy Folder

The pipeline deploys to:

```text
/opt/fastapi-react-todo
```

To change this, edit this variable in `azure-pipelines.yml`:

```yaml
variables:
  vmDeployPath: /opt/fastapi-react-todo
```

## App URLs After Deployment

Frontend:

```text
http://YOUR_VM_PUBLIC_IP
```

Backend docs:

```text
http://YOUR_VM_PUBLIC_IP:4000/docs
```

## VM Ports To Open

Open these ports in the VM firewall and Azure/network security group:

- `22` for SSH
- `80` for frontend
- `4000` for FastAPI docs/API, optional if you only want frontend access through Nginx
