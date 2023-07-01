from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "tune" DROP COLUMN "excercise_id";
        ALTER TABLE "tune" ALTER COLUMN "description" DROP NOT NULL;
        CREATE TABLE "tune_excercise" (
    "excercise_id" INT NOT NULL REFERENCES "excercise" ("id") ON DELETE CASCADE,
    "tune_id" INT NOT NULL REFERENCES "tune" ("id") ON DELETE CASCADE
);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        DROP TABLE IF EXISTS "tune_excercise";
        ALTER TABLE "tune" ADD "excercise_id" INT NOT NULL;
        ALTER TABLE "tune" ALTER COLUMN "description" SET NOT NULL;
        """