
FROM python:3.11.11-alpine3.20 AS image


FROM image AS builder


WORKDIR /code

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1


COPY ./requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt



FROM image AS runner

WORKDIR /app

COPY --from=builder /root/.local /root/.local
COPY ./app /app/app
COPY ./alembic.ini /app
COPY ./alembic /app/alembic
COPY ./tests /app/tests
COPY celery_worker.py /app
#COPY ./.env .


EXPOSE 8000
ENV PATH=/root/.local/bin:$PATH