"""empty message

Revision ID: 1ca2ec89b1a8
Revises: 05c30842dde3
Create Date: 2024-01-26 09:30:05.703188

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1ca2ec89b1a8'
down_revision = '05c30842dde3'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('resena', schema=None) as batch_op:
        batch_op.add_column(sa.Column('id_juego', sa.Integer(), nullable=False))
        batch_op.create_foreign_key(None, 'productos', ['id_juego'], ['id'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('resena', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_column('id_juego')

    # ### end Alembic commands ###