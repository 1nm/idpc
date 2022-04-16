FROM python:3.10-slim
RUN apt-get update && apt-get install -y imagemagick
COPY requirements.txt /requirements.txt
RUN pip install -r /requirements.txt && rm -f /requirements.txt
COPY idpc.py /usr/local/bin/idpc
RUN chmod +x /usr/local/bin/idpc
CMD ["/usr/local/bin/idpc"]