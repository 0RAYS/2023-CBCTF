FROM ubuntu:22.04


COPY start.sh /start.sh
RUN     apt-get update \
        && echo "#!/bin/sh\nexit 0" > /usr/sbin/policy-rc.d \
        && apt-get install -y openssh-server \
        && chmod +x /start.sh \
        && echo 'root:ascascijsnalcnsluehfwehflkjnkn'|chpasswd \
        && mkdir -p /var/run/sshd \
        && echo "PermitRootLogin yes" >> /etc/ssh/sshd_config

EXPOSE  22
CMD     ["/start.sh"]
