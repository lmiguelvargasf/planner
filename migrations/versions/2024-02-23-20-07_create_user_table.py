"""Create user table

Revision ID: 64d5792bda80
Revises: None (first migration)
Create Date: 2024-02-23 20:07:32.836670

"""
from typing import Sequence

import sqlalchemy as sa
import sqlmodel
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "64d5792bda80"
down_revision: str | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

sex_enum = sa.Enum("MALE", "FEMALE", name="sex")


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "user",
        sa.Column(
            "uuid",
            sqlmodel.sql.sqltypes.GUID(),
            server_default=sa.text("gen_random_uuid()"),
            nullable=False,
        ),
        sa.Column("first_name", sqlmodel.sql.sqltypes.AutoString(), nullable=True),
        sa.Column("middle_name", sqlmodel.sql.sqltypes.AutoString(), nullable=True),
        sa.Column("last_name", sqlmodel.sql.sqltypes.AutoString(), nullable=True),
        sa.Column(
            "second_last_name", sqlmodel.sql.sqltypes.AutoString(), nullable=True
        ),
        sa.Column("date_of_birth", sa.Date(), nullable=True),
        sa.Column("sex", sex_enum, nullable=True),
        sa.Column("email", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column("hashed_password", sqlmodel.sql.sqltypes.AutoString(), nullable=True),
        sa.Column(
            "is_active", sa.Boolean(), server_default=sa.text("true"), nullable=False
        ),
        sa.Column(
            "is_superuser",
            sa.Boolean(),
            server_default=sa.text("false"),
            nullable=False,
        ),
        sa.Column(
            "created_at",
            sa.TIMESTAMP(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.TIMESTAMP(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("uuid"),
        sa.UniqueConstraint("email"),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("user")
    sex_enum.drop(op.get_bind())
    # ### end Alembic commands ###
