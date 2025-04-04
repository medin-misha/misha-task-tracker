"""remove how_many

Revision ID: 9e84b10837ea
Revises: 47a1486840fd
Create Date: 2025-02-10 12:57:07.603363

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "9e84b10837ea"
down_revision: Union[str, None] = "47a1486840fd"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("replay", "how_many")
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "replay",
        sa.Column("how_many", sa.INTEGER(), autoincrement=False, nullable=True),
    )
    # ### end Alembic commands ###
