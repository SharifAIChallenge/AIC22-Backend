FROM reg.aichallenge.ir/python:3.8

# Set the timezone.
RUN echo "Asia/Tehran" > /etc/timezone
RUN dpkg-reconfigure -f noninteractive tzdata
RUN apt-get update

WORKDIR /code

ADD requirements.txt requirement.txt
RUN pip3 install --upgrade setuptools
RUN pip3 install -r requirements.txt

ADD . .

CMD ["gunicorn", "--bind=0.0.0.0:8000", "--timeout=90", "--preload", "AIC22_Backend.wsgi:application"]