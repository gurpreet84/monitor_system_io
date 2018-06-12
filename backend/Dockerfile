FROM python:2.7
ADD requirement.txt /monitor/
WORKDIR /monitor/
RUN pip install -r requirement.txt
COPY . /monitor/
CMD ["supervisord", "-c", "supervisor.conf"]

