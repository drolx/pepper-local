# Build file for docker daemon mode.
# ---- Base python ----
FROM python:3.13-alpine as base
# Create app directory
WORKDIR /app
# Set up and activate virtual environment
RUN apk add --no-cache --virtual build-dependencies python3-dev=3.12.8-r1 build-base=0.5-r3
ENV VIRTUAL_ENV "/app/.venv"
RUN python -m venv $VIRTUAL_ENV
ENV PATH "$VIRTUAL_ENV/bin:$PATH"

# ---- Dependencies ----
FROM base AS dependencies
COPY pyproject.toml /app
RUN pip install --no-cache-dir /app

# ---- Copy Files/Build ----
FROM dependencies AS build
WORKDIR /app
COPY . /app
# RUN python setup.py install


# --- Release with Alpine ----
FROM python:3.13-slim-buster AS release

ENV DATABASE_URL postgresql://postgres:postgres@postgres:5432/pepper
ENV API_BASE_URL https://app.protrack.ng
ENV API_USER demo@protrack.ng
ENV API_PASS tracker1234

# Create app directory
WORKDIR /app
COPY --from=dependencies /app/requirements.txt ./
COPY --from=dependencies /root/.cache /root/.cache
# Install app dependencies
RUN pip install --no-cache-dir /app
COPY --from=build /app/ ./

EXPOSE 8080

CMD ["python", "-m", "app"]
