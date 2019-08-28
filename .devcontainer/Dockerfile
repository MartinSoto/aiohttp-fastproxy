FROM adle05vp.de.top.com:5001/kpk-devshell

RUN apt-get install net-tools

RUN pip3 install \
    mypy \
    pyflakes \
    pytest \
    virtualenvwrapper \
    yapf

RUN echo 'source /usr/local/bin/virtualenvwrapper.sh' >> /root/.bashrc