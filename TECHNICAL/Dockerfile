FROM node:24-alpine
ENV NODE_ENV=production PORT=8080
WORKDIR /app
COPY --chown=node:node dashboard/ ./dashboard/
COPY --chown=node:node scripts/server.mjs ./scripts/server.mjs
USER node
EXPOSE 8080
CMD ["node", "scripts/server.mjs"]
