FROM python:3.12.10

WORKDIR /home

COPY otp.py otp.py

ENTRYPOINT ["python", "otp.py"]