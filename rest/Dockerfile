FROM python:3

# Transfer folder over to container, install the modules
COPY . /usr/src/rest
WORKDIR /usr/src/rest
RUN pip install --no-cache-dir -r requirements.txt

# Run the app
CMD ["python", "run.py"]
