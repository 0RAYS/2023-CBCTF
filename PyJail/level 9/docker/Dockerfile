FROM ubuntu:20.04

RUN sed -i "s/http:\/\/archive.ubuntu.com/http:\/\/mirrors.tuna.tsinghua.edu.cn/g" /etc/apt/sources.list && \
    apt-get update && apt-get -y dist-upgrade && \
    apt-get install -y lib32z1 xinetd && \
    apt-get install -y python3


COPY ./ctf.xinetd /etc/xinetd.d/ctf
COPY ./start.sh /

# RUN chmod +x /start.sh

COPY ./script/ /home/

RUN echo "Blocked by ctf_xinetd" > /etc/banner_fail && chmod +x /start.sh && chmod -R 777 /home/
CMD ["/start.sh"]

EXPOSE 9999
