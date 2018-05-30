FROM frolvlad/alpine-python3
COPY . /root/bot
WORKDIR /root/bot
RUN pip3 install requests
RUN pip3 install discord.py
RUN pip install py3dns
CMD python3 run.py