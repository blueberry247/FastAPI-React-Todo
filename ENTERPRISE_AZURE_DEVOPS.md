# Enterprise Azure DevOps Setup

This project now includes an enterprise-style pipeline:

```text
azure-pipelines-enterprise.yml
```

It is separate from the working VM deployment pipeline:

```text
azure-pipelines.yml
```

## What It Demonstrates

- PR validation for `main`.
- Build, test, and release stages.
- Dev, Staging, and Production stages.
- Manual approval gates before Staging and Production.
- Docker image build and push to Azure Container Registry.
- Key Vault secret loading per environment.
- Terraform `fmt`, `init`, `validate`, and `plan`.
- Security scanning with Trivy, Gitleaks, and tfsec.
- Docker image vulnerability scanning that fails on high and critical findings.
- Resource tagging and ACR retention policy in Terraform.

## Required Azure DevOps Service Connections

Create these in Azure DevOps `Project settings` -> `Service connections`:

```text
fastapi-azure-sp
```

Type: Azure Resource Manager.

Used by Terraform, Key Vault, and App Service deployment.

```text
fastapi-acr
```

Type: Docker Registry / Azure Container Registry.

Used by Docker tasks to push images.

## Required Variables To Change

Edit `azure-pipelines-enterprise.yml`:

```yaml
acrLoginServer: CHANGE_ME.azurecr.io
devKeyVaultName: kv-fastapi-dev
stagingKeyVaultName: kv-fastapi-staging
prodKeyVaultName: kv-fastapi-prod
```

## Terraform Remote State

The Terraform backend is configured in:

```text
infra/versions.tf
```

You need an Azure Storage Account and Blob container for remote state.

Example init command:

```bash
terraform init \
  -backend-config="resource_group_name=rg-tfstate" \
  -backend-config="storage_account_name=sttfstateexample" \
  -backend-config="container_name=tfstate" \
  -backend-config="key=fastapi-react-todo.tfstate"
```

## Important Note

This is a professional scaffold. Before running it live, replace all `CHANGE_ME` values and confirm your Azure subscription permissions, App Service names, ACR name, and Key Vault names.

Your existing VM pipeline still works and should be kept for the current deployed app.
