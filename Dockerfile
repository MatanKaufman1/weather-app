FROM python:3.11.9-slim AS build
WORKDIR /app/
COPY requirements.txt /app
RUN python -m venv /app/venv
RUN . /app/venv/bin/activate && \
    pip install --upgrade pip && \
    pip install -r requirements.txt
COPY src/ /app/


FROM python:3.11.9-slim AS deploy
WORKDIR /app
COPY --from=build app/ /app
ENV PATH="/app/venv/bin:$PATH"
RUN useradd -ms /bin/bash appuser
RUN chown -R appuser:appuser /app /home/appuser/
USER appuser
EXPOSE 5000
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "wsgi:app"]
