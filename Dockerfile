FROM python:3.13-slim-bookworm AS base
WORKDIR /app
RUN  apt-get update && \
  apt-get upgrade -y && \
  apt-get install --no-install-recommends -y build-essential python3-dev
ENV VIRTUAL_ENV="/app/.venv"
RUN python -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# ---- Dependencies ----
FROM base AS build
WORKDIR /app
COPY . .
RUN make install && \
  make bundle

# --- Release with Alpine ----
FROM debian:bookworm-slim AS release

ENV DATABASE_URL=postgresql://postgres:postgres@postgres:5432/pepper
ENV API_BASE_URL=https://app.example.com
ENV API_USER=demo@example.com
ENV API_PASS=password 
ENV GEOCODE_URL=https://nominatim.openstreetmap.org
ENV FETCH_INTERVAL=630
ENV OFFLINE_INTERVAL=90

# Create app directory
WORKDIR /app
COPY --from=build /app/dist .
RUN apt-get update && \
  apt-get upgrade -y && \
  apt-get install -y curl && \
  apt-get clean

EXPOSE 8080
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=5 CMD curl --fail http://localhost:8080/ || exit 1

CMD ["/app/pepper-local"]
