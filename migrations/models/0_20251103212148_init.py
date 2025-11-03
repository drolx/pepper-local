from tortoise import BaseDBAsyncClient

RUN_IN_TRANSACTION = True


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "address" (
    "id" CHAR(36) NOT NULL PRIMARY KEY,
    "created_at" TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP /* The date-time the Device record was created at */,
    "modified_at" TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP /* The date-time the Device record was modified at */,
    "name" VARCHAR(1024) NOT NULL,
    "lat" REAL NOT NULL,
    "lon" REAL NOT NULL,
    "attributes" JSON NOT NULL
);
CREATE TABLE IF NOT EXISTS "devices" (
    "id" CHAR(36) NOT NULL PRIMARY KEY,
    "created_at" TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP /* The date-time the Device record was created at */,
    "modified_at" TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP /* The date-time the Device record was modified at */,
    "position_id" CHAR(36),
    "resolver" VARCHAR(128) NOT NULL,
    "name" VARCHAR(128) NOT NULL,
    "time" TIMESTAMP,
    "unique_id" VARCHAR(128) NOT NULL UNIQUE,
    "status" VARCHAR(64) NOT NULL /* UNKNOWN: unknown\nOFFLINE: offline\nMOVING: moving\nPARKED: parked\nIDLING: idling */,
    "odometer" REAL,
    "moved_at" TIMESTAMP,
    "stopped_at" TIMESTAMP,
    "battery" REAL,
    "charging" INT NOT NULL DEFAULT 0
);
CREATE INDEX IF NOT EXISTS "idx_devices_positio_69bae6" ON "devices" ("position_id");
CREATE INDEX IF NOT EXISTS "idx_devices_resolve_bcd35e" ON "devices" ("resolver");
CREATE INDEX IF NOT EXISTS "idx_devices_time_d6d030" ON "devices" ("time");
CREATE INDEX IF NOT EXISTS "idx_devices_unique__8dd8ba" ON "devices" ("unique_id");
CREATE INDEX IF NOT EXISTS "idx_devices_moved_a_ef882e" ON "devices" ("moved_at");
CREATE INDEX IF NOT EXISTS "idx_devices_stopped_c9204a" ON "devices" ("stopped_at");
CREATE TABLE IF NOT EXISTS "events" (
    "id" CHAR(36) NOT NULL PRIMARY KEY,
    "tag" VARCHAR(64) NOT NULL,
    "type" VARCHAR(64) NOT NULL /* OVERSPEED: overspeed\nGEOFENCE_IN: geofence_in\nGEOFENCE_OUT: geofence_out\nPOWER_LOSS: power_loss\nTAMPER: tamper */,
    "device_id" CHAR(36) NOT NULL,
    "position_id" CHAR(36) NOT NULL,
    "time" TIMESTAMP NOT NULL,
    "fix_time" TIMESTAMP NOT NULL,
    "attributes" JSON NOT NULL
);
CREATE INDEX IF NOT EXISTS "idx_events_device__86a0b0" ON "events" ("device_id");
CREATE INDEX IF NOT EXISTS "idx_events_positio_f41252" ON "events" ("position_id");
CREATE TABLE IF NOT EXISTS "geofences" (
    "id" CHAR(36) NOT NULL PRIMARY KEY,
    "created_at" TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP /* The date-time the Device record was created at */,
    "modified_at" TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP /* The date-time the Device record was modified at */,
    "name" VARCHAR(128) NOT NULL,
    "details" VARCHAR(1924),
    "geometry" JSON NOT NULL
);
CREATE TABLE IF NOT EXISTS "positions" (
    "id" CHAR(36) NOT NULL PRIMARY KEY,
    "resolver" VARCHAR(128) NOT NULL,
    "valid" INT NOT NULL DEFAULT 1,
    "device_id" CHAR(36),
    "time" TIMESTAMP NOT NULL,
    "fix_time" TIMESTAMP NOT NULL,
    "speed" REAL NOT NULL,
    "lat" REAL NOT NULL,
    "lon" REAL NOT NULL,
    "course" REAL NOT NULL,
    "altitude" REAL NOT NULL,
    "address" VARCHAR(1024),
    "odometer" REAL,
    "battery" REAL,
    "charging" INT NOT NULL DEFAULT 0,
    "attributes" JSON NOT NULL
);
CREATE INDEX IF NOT EXISTS "idx_positions_device__2a967e" ON "positions" ("device_id");
CREATE TABLE IF NOT EXISTS "server_events" (
    "id" CHAR(36) NOT NULL PRIMARY KEY,
    "tag" VARCHAR(64) NOT NULL,
    "type" VARCHAR(64) NOT NULL /* OVERSPEED: overspeed */,
    "time" TIMESTAMP NOT NULL,
    "attributes" JSON NOT NULL
);
CREATE TABLE IF NOT EXISTS "users" (
    "id" CHAR(36) NOT NULL PRIMARY KEY,
    "created_at" TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP /* The date-time the Device record was created at */,
    "modified_at" TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP /* The date-time the Device record was modified at */,
    "full_name" VARCHAR(256) NOT NULL,
    "email" VARCHAR(128) NOT NULL,
    "role" VARCHAR(64) NOT NULL DEFAULT 'user' /* ADMIN: admin\nUSER: user */,
    "phone" VARCHAR(15) NOT NULL,
    "password_hash" VARCHAR(1024) NOT NULL
);
CREATE TABLE IF NOT EXISTS "aerich" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    "version" VARCHAR(255) NOT NULL,
    "app" VARCHAR(100) NOT NULL,
    "content" JSON NOT NULL
);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        """


MODELS_STATE = (
    "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"
)
