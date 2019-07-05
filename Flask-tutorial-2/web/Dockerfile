FROM python:3.7-alpine
WORKDIR /usr/src/app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
RUN chmod 644 __init__.py
CMD ["python", "__init__.py"]