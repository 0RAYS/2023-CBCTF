FROM node:18.1.0-bullseye-slim


COPY src/ /app/

WORKDIR /app/

RUN npm install --registry https://registry.npm.taobao.org 

CMD ["node", "server.js"]