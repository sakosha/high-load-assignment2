FROM python:3.11

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

WORKDIR /app

RUN pip install uv

COPY requirements.txt /app/
RUN uv pip install --system -r requirements.txt

COPY my_blog/ /app/

CMD ["gunicorn", "my_blog.wsgi:application", "--bind", "0.0.0.0:8000"]
