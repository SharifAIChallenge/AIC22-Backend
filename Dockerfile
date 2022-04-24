FROM registry.cafebazaar.ir:5000/divar/infra/common-images:python3.8

# Set the timezone.
RUN echo "Asia/Tehran" > /etc/timezone
RUN dpkg-reconfigure -f noninteractive tzdata
RUN apt-get update

WORKDIR /code

ADD ./requirement.txt /code/requirement.txt
RUN pip3 install --upgrade setuptools
RUN pip3 install -r requirement.txt

ADD . /code

CMD ["gunicorn", "--bind=0.0.0.0:8000", "--timeout=90", "--preload", "AIC22_Backend.wsgi:application"]