"""empty message

Revision ID: 101f44947717
Revises: 6e21e9085a6c
Create Date: 2024-06-18 17:52:35.548368

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "101f44947717"
down_revision: Union[str, None] = "6e21e9085a6c"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
