FROM python:3.14.2

WORKDIR /home

COPY otp.py otp.py

ENTRYPOINT ["python", "otp.py"]