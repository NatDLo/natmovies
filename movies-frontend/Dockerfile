FROM node:22-alpine

WORKDIR /app

# Install deps
COPY package*.json ./
RUN npm ci

# Copy source
COPY . .

EXPOSE 4200

# Dev server with hot reload inside container
CMD ["npm", "run", "start", "--", "--host", "0.0.0.0", "--port", "4200"]