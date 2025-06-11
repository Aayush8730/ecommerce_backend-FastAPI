"""add the product table

Revision ID: a0d56d1f4df6
Revises: 4da3e75eb4f7
Create Date: 2025-06-11 13:00:13.712665

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a0d56d1f4df6'
down_revision: Union[str, None] = '4da3e75eb4f7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
