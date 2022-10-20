FROM ubuntu:20.04
RUN apt update -y && apt upgrade -y && apt install python3 -y
RUN apt install python3-pip -y
COPY * .
RUN pip install -r requirements.txt
RUN ls
CMD export FLASK_APP=start
CMD flask run
