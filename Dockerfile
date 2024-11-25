FROM python:3.14.0a1-slim

# USER app
ENV PYTHONUNBUFFERED 1
# RUN mkdir /db
#RUN chown app:app -R /db

RUN mkdir /code
WORKDIR /code
ADD requirements.txt /code/
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt
ADD . /code/
CMD ["/bin/bash", "./main.sh"]