FROM python:3.7
WORKDIR /usr/src/app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .

# app.py is executable, so set owner permissions to read/write and group members read-only
# some systems may require shebang of '#!/usr/bin/env python3' or alike
RUN chmod 644 app.py
CMD ["python", "app.py"]