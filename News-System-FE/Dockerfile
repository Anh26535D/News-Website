FROM node:20.10.0-slim AS builder

WORKDIR /app
COPY package.json ./
RUN npm install

FROM node:20.10.0-slim

WORKDIR /app
COPY --from=builder /app/package-lock.json ./
COPY --from=builder /app/node_modules ./
COPY . .

RUN npm install

CMD ["npm", "start"]
