FROM ubuntu:latest

ADD orn.py .
RUN pip install requests 
RUN pip install pyrebase

CMD ["python", "orn.py"]