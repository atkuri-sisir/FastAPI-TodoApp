"""Create phone number column for users

Revision ID: 8fdc1a54fa32
Revises: 
Create Date: 2026-05-03 11:03:57.138367

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8fdc1a54fa32'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('users', sa.Column('phone_number', sa.String(15), nullable=True))


def downgrade() -> None:
    """Downgrade schema."""
    pass
