FROM node:20

WORKDIR /app

COPY app/ .
COPY readflag.c /readflag.c
COPY start.sh /start.sh

RUN npm install
RUN gcc -o /readflag /readflag.c
RUN chmod u+s /readflag
RUN chown -R node:node /app
RUN chmod +x /start.sh

EXPOSE 1337

CMD [ "/start.sh" ]
