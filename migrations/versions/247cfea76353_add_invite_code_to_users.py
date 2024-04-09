"""Add invite code to users

Revision ID: 247cfea76353
Revises: ef2d426de61b
Create Date: 2024-04-09 12:33:29.647597

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '247cfea76353'
down_revision = 'ef2d426de61b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user_accounts', schema=None) as batch_op:
        batch_op.add_column(sa.Column('invite_code', sa.String(length=128), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user_accounts', schema=None) as batch_op:
        batch_op.drop_column('invite_code')

    # ### end Alembic commands ###
