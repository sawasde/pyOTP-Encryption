FROM python:3.8

WORKDIR /home

COPY otp.py otp.py

ENTRYPOINT ["python", "otp.py"]