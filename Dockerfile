FROM python:3.13.3

WORKDIR /home

COPY otp.py otp.py

ENTRYPOINT ["python", "otp.py"]