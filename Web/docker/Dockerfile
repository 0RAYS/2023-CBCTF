FROM node:17-alpine

RUN mkdir /src

WORKDIR /src

RUN sed -i 's/dl-cdn.alpinelinux.org/mirrors.ustc.edu.cn/g' /etc/apk/repositories
RUN apk update && apk upgrade
RUN apk add chromium
RUN npm install express puppeteer cors --registry=https://registry.npmmirror.com/

COPY src /src
WORKDIR /src

EXPOSE 3000

CMD ["node", "bot_server.js"]
