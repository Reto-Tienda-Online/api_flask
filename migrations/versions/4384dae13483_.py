"""empty message

Revision ID: 4384dae13483
Revises: 24b26be01d3b
Create Date: 2024-01-22 08:52:20.002614

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4384dae13483'
down_revision = '24b26be01d3b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('tipopago',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('tipopago', sa.String(length=50), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('metodopago', schema=None) as batch_op:
        batch_op.add_column(sa.Column('nombreCompleto', sa.String(length=60), nullable=False))
        batch_op.add_column(sa.Column('id_metodo', sa.Integer(), nullable=False))
        batch_op.create_foreign_key(None, 'tipopago', ['id_metodo'], ['id'])
        batch_op.drop_column('metodo')

    with op.batch_alter_table('productos', schema=None) as batch_op:
        batch_op.add_column(sa.Column('rutatrailer', sa.String(length=255), nullable=False))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('productos', schema=None) as batch_op:
        batch_op.drop_column('rutatrailer')

    with op.batch_alter_table('metodopago', schema=None) as batch_op:
        batch_op.add_column(sa.Column('metodo', sa.VARCHAR(length=60), autoincrement=False, nullable=False))
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_column('id_metodo')
        batch_op.drop_column('nombreCompleto')

    op.drop_table('tipopago')
    # ### end Alembic commands ###
