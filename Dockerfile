FROM ubuntu:20.04
RUN apt update -y && apt upgrade -y && apt install python3 -y
RUN apt install python3-pip -y
RUN git clone https://github.com/wzk0/simple-wyy && cd simply-wyy
RUN pip install -r requirements.txt
CMD export FLASK_APP=start && export FLASK_ENV=development && flask run --host=0.0.0.0 --port=$PORT