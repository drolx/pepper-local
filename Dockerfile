FROM ghcr.io/astral-sh/uv:python3.12-trixie-slim AS builder

ENV UV_LINK_MODE=copy \
    UV_COMPILE_BYTECODE=1 \
    UV_PYTHON_DOWNLOADS=never \
    UV_NO_DEV=1 \
    UV_HTTP_TIMEOUT=900 \
    UV_PROJECT_ENVIRONMENT=/app/.venv

# Print Python and uv version for debugging
RUN python --version && which python && uv --version

WORKDIR /app

COPY . /app
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-dev

FROM python:3.12-slim-trixie AS runtime

LABEL org.opencontainers.image.source=https://github.com/drolx/pepper-local
LABEL org.opencontainers.image.description="Pepper Sync"
LABEL org.opencontainers.image.licenses=MIT

RUN apt-get update && \
  apt-get upgrade -y && \
  apt-get install -y curl && \
  apt-get clean

# Setup a non-root user
RUN groupadd --system --gid 999 nonroot \
 && useradd --system --gid 999 --uid 999 --create-home nonroot

WORKDIR /app

RUN chown -R nonroot:nonroot /app

USER nonroot

COPY --from=builder --chown=nonroot:nonroot /app /app

ENV PATH="/app/.venv/bin:$PATH"
ENV PYTHONUNBUFFERED=1

EXPOSE 8000
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=5 CMD curl --fail http://localhost:8000/api/server || exit 1

ENTRYPOINT []

CMD ["uvicorn", "pepper.server:app", "--host", "0.0.0.0", "--port", "8000"]
