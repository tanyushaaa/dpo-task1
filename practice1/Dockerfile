FROM python:3
LABEL maintainer="zotovvvat@yandex.ru"
COPY ./botcontrol.py /
COPY ./path.txt
RUN sudo yum -y install epel-release
RUN sudo systemctl start mosquitto
RUN sudo systemctl enable mosquitto
CMD ["./botcontrol.py"]
