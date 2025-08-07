FROM python:3.13-slim
RUN pip install --upgrade uv

WORKDIR /app
COPY . /app

RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync

CMD ["uv", "run", "python", "-m", "src.main"]