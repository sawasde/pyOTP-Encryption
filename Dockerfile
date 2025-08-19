FROM python:3.14.0rc2

WORKDIR /home

COPY otp.py otp.py

ENTRYPOINT ["python", "otp.py"]