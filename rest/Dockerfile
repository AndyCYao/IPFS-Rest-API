FROM python:3
MAINTAINER  Andy Yao  <andyyao3@gmail.com>

WORKDIR /usr/src/app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Run the app
CMD ["python", "app.py"]
