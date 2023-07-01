from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "suggestion" ALTER COLUMN "suggester_id" DROP NOT NULL;
        ALTER TABLE "user" ADD "last_activity" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "user" DROP COLUMN "last_activity";
        ALTER TABLE "suggestion" ALTER COLUMN "suggester_id" SET NOT NULL;"""
