



**logged in** 

az acr login --name taskappacr247



**Then tag the backend**



docker tag taskapp\_backend:latest taskappacr247.azurecr.io/taskapp\_backend:latest



**frontend** 



**Tag the frontend:**



docker tag taskapp\_frontend:latest taskappacr247.azurecr.io/taskapp\_frontend:latest



**Check:**



**docker images**



**Then push the backend:**



docker push taskappacr247.azurecr.io/taskapp\_backend:latest



A**nd push the frontend:**



docker push taskappacr247.azurecr.io/taskapp\_frontend:latest



**That doesn't tell Docker which registry it should be uploaded to.**

**So we create another tag:**



docker tag taskapp\_backend:latest taskappacr247.azurecr.io/taskapp\_backend:latest



docker tag taskapp\_frontend:latest taskappacr247.azurecr.io/taskapp\_frontend:latest



taskappacr247.azurecr.io/taskapp\_backend:latest

│

│ Registry

│

├─────────────────────┐

&#x20;                     ↓

&#x20;               Repository

&#x20;               taskapp\_backend

&#x20;                     ↓

&#x20;                   latest

&#x20;                    Tag



**You should see entries like:**



taskapp\_backend

taskapp\_frontend

taskappacr247.azurecr.io/taskapp\_backend

taskappacr247.azurecr.io/taskapp\_frontend



**Then push the backend**

docker push taskappacr247.azurecr.io/taskapp\_backend:latest



**Then push the frontend:**

**docker push taskappacr247.azurecr.io/taskapp\_frontend:latest**





**https://taskapp-backend247-cmcvfxcebsg9gbdy.ukwest-01.azurewebsites.net/docs?utm\_source=chatgpt.com**



**https://taskapp-web247-gjazetedardrd6au.ukwest-01.azurewebsites.net**





## **Node Package Manager.**



**# Show which version of npm is installed.**



npm.cmd --version



**# Show where the "ws" package is installed in the dependency tree.**

**# "ws" is a WebSocket library used by many React/dev-server packages.**



npm.cmd ls ws



**# Check installed npm packages for known security vulnerabilities.**

**# This reads package-lock.json/node\_modules and reports low/medium/high/critical issues.**



npm.cmd audit



**# Same as above: show where the "ws" package is installed.**

**# This is duplicated, so you only need to run it once.**



npm.cmd ls ws







