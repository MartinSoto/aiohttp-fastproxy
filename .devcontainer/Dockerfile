FROM martinsoto/devshell-python

COPY requirements.txt /tmp/requirements.txt
RUN pip3 install -r /tmp/requirements.txt && \
    rm /tmp/requirements.txt
