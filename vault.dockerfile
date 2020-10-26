FROM vault:1.5.3
ENV VAULT_URL=http://127.0.0.1:8200
RUN apk add --update --no-cache python3 bash curl && \
    if [ ! -e /usr/bin/python ]; then ln -sf python3 /usr/bin/python ; fi && \
    python3 -m ensurepip && \
    rm -r /usr/lib/python*/ensurepip && \
    pip3 install --no-cache --upgrade pip && \
    pip3 install --no-cache requests jinja2
RUN mkdir -p /data/vault
RUN mkdir -p /etc/vault
COPY ./config/vault/vault.hcl.j2 /tmp/vault.hcl.j2
COPY  ./config/vault/docker-entrypoint.py /usr/local/bin/docker-entrypoint.py
ENV VAULT_SKIP_VERIFY=true
ENTRYPOINT [ "python","/usr/local/bin/docker-entrypoint.py", "-l", "DEBUG"]