# Build stage: compile the React app into static production files.
FROM node:20-alpine AS build

WORKDIR /app

# Install exact dependencies from package-lock.json.
COPY package*.json ./
RUN npm ci

# Copy React source and build it.
COPY . .
RUN npm run build

# Runtime stage: serve the built React app with Nginx.
FROM nginx:1.27-alpine

# Custom Nginx config serves React and proxies API routes to FastAPI.
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Copy the compiled React build into Nginx's web root.
COPY --from=build /app/build /usr/share/nginx/html

EXPOSE 80

# Keep Nginx running in the foreground for Docker.
CMD ["nginx", "-g", "daemon off;"]