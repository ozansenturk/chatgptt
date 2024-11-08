# frontend/Dockerfile

# Use official Node.js image to build the app
FROM node:18 AS build

# Set working directory in the container
WORKDIR /app

# Copy package.json and install dependencies
COPY package.json ./
RUN npm install

# Copy all files and build the app
COPY . .
RUN npm run build

# Use a lightweight web server to serve the static files
FROM nginx:alpine
COPY --from=build /app/build /usr/share/nginx/html

# Expose port for the frontend
EXPOSE 80

# Nginx will serve the React app by default
CMD ["nginx", "-g", "daemon off;"]
