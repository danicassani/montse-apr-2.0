from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "excercise" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "title" VARCHAR(100) NOT NULL UNIQUE,
    "description" VARCHAR(1000) NOT NULL,
    "difficulty" INT NOT NULL  DEFAULT 0
);
CREATE TABLE IF NOT EXISTS "user" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "discord_user_id" BIGINT NOT NULL UNIQUE,
    "user_name" VARCHAR(100) NOT NULL,
    "experience" INT NOT NULL  DEFAULT 0,
    "register_date" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE IF NOT EXISTS "levelperformance" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "trials" INT NOT NULL  DEFAULT 0,
    "successes" INT NOT NULL  DEFAULT 0,
    "last_tried" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "user_id" INT NOT NULL REFERENCES "user" ("id") ON DELETE RESTRICT
);
CREATE TABLE IF NOT EXISTS "chordrecognitionlevel" (
    "level_number" SERIAL NOT NULL PRIMARY KEY,
    "description" VARCHAR(1000) NOT NULL,
    "chord_type" VARCHAR(100) NOT NULL,
    "shape" VARCHAR(100) NOT NULL,
    "inversion" VARCHAR(100) NOT NULL,
    "performance_id" INT REFERENCES "levelperformance" ("id") ON DELETE RESTRICT
);
CREATE TABLE IF NOT EXISTS "frequencyrecognitionlevel" (
    "level_number" SERIAL NOT NULL PRIMARY KEY,
    "description" VARCHAR(1000) NOT NULL,
    "frequency_thresholds" VARCHAR(100) NOT NULL,
    "performance_id" INT REFERENCES "levelperformance" ("id") ON DELETE RESTRICT
);
CREATE TABLE IF NOT EXISTS "intervalrecognitionlevel" (
    "level_number" SERIAL NOT NULL PRIMARY KEY,
    "description" VARCHAR(1000) NOT NULL,
    "interval" INT NOT NULL  DEFAULT 0,
    "direction" VARCHAR(100) NOT NULL,
    "performance_id" INT REFERENCES "levelperformance" ("id") ON DELETE RESTRICT
);
CREATE TABLE IF NOT EXISTS "melodicdictationlevel" (
    "level_number" SERIAL NOT NULL PRIMARY KEY,
    "description" VARCHAR(1000) NOT NULL,
    "length" INT NOT NULL  DEFAULT 0,
    "time_signature" VARCHAR(100) NOT NULL  DEFAULT '4/4',
    "performance_id" INT REFERENCES "levelperformance" ("id") ON DELETE RESTRICT
);
CREATE TABLE IF NOT EXISTS "moderecognitionlevel" (
    "level_number" SERIAL NOT NULL PRIMARY KEY,
    "description" VARCHAR(1000) NOT NULL,
    "name" VARCHAR(100) NOT NULL,
    "shape" VARCHAR(100) NOT NULL,
    "characteristic_notes" VARCHAR(100) NOT NULL,
    "presentation" VARCHAR(100) NOT NULL,
    "performance_id" INT REFERENCES "levelperformance" ("id") ON DELETE RESTRICT
);
CREATE TABLE IF NOT EXISTS "phrase" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "content" VARCHAR(300) NOT NULL,
    "context" VARCHAR(1000) NOT NULL,
    "date" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "author_id" INT NOT NULL REFERENCES "user" ("id") ON DELETE RESTRICT,
    "reviewer_id" INT REFERENCES "user" ("id") ON DELETE RESTRICT
);
CREATE TABLE IF NOT EXISTS "suggestion" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "title" VARCHAR(200) NOT NULL,
    "content" VARCHAR(2000) NOT NULL,
    "resolution" VARCHAR(2000),
    "date" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "reviewer_id" INT REFERENCES "user" ("id") ON DELETE RESTRICT,
    "suggester_id" INT NOT NULL REFERENCES "user" ("id") ON DELETE RESTRICT
);
CREATE TABLE IF NOT EXISTS "tune" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "title" VARCHAR(200) NOT NULL,
    "description" VARCHAR(1000) NOT NULL,
    "date" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "author_id" INT NOT NULL REFERENCES "user" ("id") ON DELETE RESTRICT,
    "excercise_id" INT NOT NULL REFERENCES "excercise" ("id") ON DELETE RESTRICT,
    CONSTRAINT "uid_tune_author__4adbf4" UNIQUE ("author_id", "title")
);
CREATE TABLE IF NOT EXISTS "warning" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "reason" VARCHAR(200) NOT NULL,
    "message" VARCHAR(1000) NOT NULL,
    "date" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "user_id" INT NOT NULL REFERENCES "user" ("id") ON DELETE RESTRICT
);
CREATE TABLE IF NOT EXISTS "aerich" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "version" VARCHAR(255) NOT NULL,
    "app" VARCHAR(100) NOT NULL,
    "content" JSONB NOT NULL
);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        """
