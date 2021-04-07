FROM fedora:33
LABEL Maintainer="Zainab Alsaffar <@zanssa>" \
      Description="Ansible & Ansible Tower CLI"

RUN dnf install -y \
    ansible \
    python3-pip \
    && pip3 install awxkit \
    && dnf -y clean all \
    && rm -rf /tmp/*

ADD tower.sh /tmp/tower.sh

RUN chmod +x /tmp/tower.sh

ENTRYPOINT [ "/tmp/tower.sh" ]