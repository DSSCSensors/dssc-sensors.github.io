"""Add biblio

Revision ID: 5626ea423bf1
Revises: 2e1182ee5492
Create Date: 2016-03-14 00:49:26.557957

"""

# revision identifiers, used by Alembic.
revision = '5626ea423bf1'
down_revision = '2e1182ee5492'

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('cde_job', sa.Column('biblio', postgresql.JSONB(), nullable=True))
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('cde_job', 'biblio')
    ### end Alembic commands ###
