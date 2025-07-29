FROM python:3.14.0rc1

WORKDIR /home

COPY otp.py otp.py

ENTRYPOINT ["python", "otp.py"]