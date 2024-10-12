FROM python:3.11-slim

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

WORKDIR /app

# uv pip compile --universal requirements.in -o requirements.txt
# uv pip install -r requirements.txt

RUN pip install --no-cache-dir uv

COPY requirements.txt requirements.txt
RUN uv pip install --system --no-cache-dir -r requirements.txt

COPY . /app/

EXPOSE 8000

# I don't like uwsgi & gunicorn requires other services (i. e. nginx) to serve static files
#CMD ["gunicorn", "HighLoadAssignment2.wsgi:application", "--bind", "0.0.0.0:8000"]
CMD ["python", "manage.py", "runserver",  "0.0.0.0:8000"]
