FROM python:3.12-slim-trixie AS builder
COPY --from=ghcr.io/astral-sh/uv:0.9 /uv /uvx /bin/

WORKDIR /app

ENV UV_COMPILE_BYTECODE=1 UV_LINK_MODE=copy
ENV UV_TOOL_BIN_DIR=/usr/local/bin

COPY **/*.toml uv.lock /app/
RUN --mount=type=cache,target=/root/.cache/uv \
    uv lock --upgrade && \
    uv sync --locked --no-install-project --no-dev

COPY . /app
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --locked --no-dev

FROM python:3.12-slim-trixie AS runtime

LABEL org.opencontainers.image.source=https://github.com/drolx/pepper-local
LABEL org.opencontainers.image.description="Pepper Sync"
LABEL org.opencontainers.image.licenses=MIT

RUN groupadd --system --gid 999 nonroot \
 && useradd --system --gid 999 --uid 999 --create-home nonroot

RUN apt-get update && \
  apt-get upgrade -y && \
  apt-get install -y curl && \
  apt-get clean

WORKDIR /app
COPY --from=builder --chown=nonroot:nonroot /app /app

EXPOSE 8000
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=5 CMD curl --fail http://localhost:8000/api/server || exit 1

RUN chown -R nonroot:nonroot /app
USER nonroot

ENV PATH="/app/.venv/bin:$PATH"
ENTRYPOINT []

CMD ["uvicorn", "pepper.server:app", "--host", "0.0.0.0", "--port", "8000"]
