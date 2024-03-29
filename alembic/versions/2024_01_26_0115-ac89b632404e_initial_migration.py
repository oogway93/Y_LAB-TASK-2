"""initial migration

Revision ID: ac89b632404e
Revises:
Create Date: 2024-01-26 01:15:10.195861

"""
from typing import Sequence

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = 'ac89b632404e'
down_revision: str | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('menus',
                    sa.Column('id', sa.UUID(), nullable=False),
                    sa.Column('title', sa.String(), nullable=True),
                    sa.Column('description', sa.String(), nullable=True),
                    sa.PrimaryKeyConstraint('id')
                    )
    op.create_index(op.f('ix_menus_id'), 'menus', ['id'], unique=False)
    op.create_table('submenus',
                    sa.Column('id', sa.UUID(), nullable=False),
                    sa.Column('title', sa.String(), nullable=True),
                    sa.Column('description', sa.String(), nullable=True),
                    sa.Column('menu_id', sa.UUID(), nullable=True),
                    sa.ForeignKeyConstraint(['menu_id'], ['menus.id'], ondelete='CASCADE'),
                    sa.PrimaryKeyConstraint('id')
                    )
    op.create_index(op.f('ix_submenus_id'), 'submenus', ['id'], unique=False)
    op.create_table('dishes',
                    sa.Column('id', sa.UUID(), nullable=False),
                    sa.Column('title', sa.String(), nullable=True),
                    sa.Column('description', sa.String(), nullable=True),
                    sa.Column('price', sa.Numeric(), nullable=True),
                    sa.Column('submenu_id', sa.UUID(), nullable=True),
                    sa.ForeignKeyConstraint(['submenu_id'], ['submenus.id'], ondelete='CASCADE'),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('title')
                    )
    op.create_index(op.f('ix_dishes_id'), 'dishes', ['id'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_dishes_id'), table_name='dishes')
    op.drop_table('dishes')
    op.drop_index(op.f('ix_submenus_id'), table_name='submenus')
    op.drop_table('submenus')
    op.drop_index(op.f('ix_menus_id'), table_name='menus')
    op.drop_table('menus')
    # ### end Alembic commands ###
