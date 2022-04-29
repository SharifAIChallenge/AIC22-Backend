FROM docker.repos.balad.ir/python:3.8

# Set the timezone.
RUN echo "Asia/Tehran" > /etc/timezone
RUN dpkg-reconfigure -f noninteractive tzdata
RUN apt-get update

RUN apt-get -y install netcat --fix-missing

WORKDIR /code

ADD requirements.txt /code/requirements.txt
RUN pip3 install --upgrade setuptools
RUN pip3 install -r requirements.txt

ADD . /code

CMD ["bash", "entry.sh"]