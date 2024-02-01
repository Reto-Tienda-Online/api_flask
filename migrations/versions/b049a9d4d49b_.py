"""empty message

Revision ID: b049a9d4d49b
Revises: 1ca2ec89b1a8
Create Date: 2024-02-01 08:48:03.507234

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b049a9d4d49b'
down_revision = '1ca2ec89b1a8'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('tipopago')
    with op.batch_alter_table('metodopago', schema=None) as batch_op:
        batch_op.add_column(sa.Column('tipo', sa.String(length=50), nullable=False))
        batch_op.drop_constraint('metodopago_id_metodo_fkey', type_='foreignkey')
        batch_op.drop_constraint('metodopago_id_usuario_fkey', type_='foreignkey')
        batch_op.drop_column('cvv')
        batch_op.drop_column('fecha_caduc')
        batch_op.drop_column('direccion_fact')
        batch_op.drop_column('id_metodo')
        batch_op.drop_column('titular_tarjeta')
        batch_op.drop_column('nombreCompleto')
        batch_op.drop_column('numero_tarjeta')
        batch_op.drop_column('id_usuario')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('metodopago', schema=None) as batch_op:
        batch_op.add_column(sa.Column('id_usuario', sa.INTEGER(), autoincrement=False, nullable=False))
        batch_op.add_column(sa.Column('numero_tarjeta', sa.VARCHAR(length=24), autoincrement=False, nullable=False))
        batch_op.add_column(sa.Column('nombreCompleto', sa.VARCHAR(length=60), autoincrement=False, nullable=False))
        batch_op.add_column(sa.Column('titular_tarjeta', sa.VARCHAR(length=40), autoincrement=False, nullable=False))
        batch_op.add_column(sa.Column('id_metodo', sa.INTEGER(), autoincrement=False, nullable=False))
        batch_op.add_column(sa.Column('direccion_fact', sa.VARCHAR(length=255), autoincrement=False, nullable=False))
        batch_op.add_column(sa.Column('fecha_caduc', sa.INTEGER(), autoincrement=False, nullable=False))
        batch_op.add_column(sa.Column('cvv', sa.INTEGER(), autoincrement=False, nullable=False))
        batch_op.create_foreign_key('metodopago_id_usuario_fkey', 'usuarios', ['id_usuario'], ['id'])
        batch_op.create_foreign_key('metodopago_id_metodo_fkey', 'tipopago', ['id_metodo'], ['id'])
        batch_op.drop_column('tipo')

    op.create_table('tipopago',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('tipopago', sa.VARCHAR(length=50), autoincrement=False, nullable=False),
    sa.PrimaryKeyConstraint('id', name='tipopago_pkey')
    )
    # ### end Alembic commands ###
