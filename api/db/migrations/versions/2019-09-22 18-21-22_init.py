"""init

Revision ID: d3d0753d7f43
Revises: 
Create Date: 2019-09-22 18:21:22.426731

"""
import sqlalchemy_utils
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
import common

revision = 'd3d0753d7f43'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('signs',
                    sa.Column('id', sqlalchemy_utils.types.uuid.UUIDType(), nullable=False),
                    sa.Column('packet_type', sa.Enum('IP', 'TCP', 'HTTP', name='packettype'), nullable=False),
                    sa.Column('src', sa.Enum('EXTERNAL', 'HOME', name='nettype'), nullable=False),
                    sa.Column('dst', sa.Enum('EXTERNAL', 'HOME', name='nettype'), nullable=False),
                    sa.Column('checked_fields', common.db.data_types.Json(), nullable=True),
                    sa.Column('name', sa.String(), nullable=False),
                    sa.Column('result_criteria', sa.Enum('ALL', 'AT_LEAST_ONE', name='criterion'), nullable=False),
                    sa.PrimaryKeyConstraint('id')
                    )
    op.create_table('attack_events',
                    sa.Column('id', sqlalchemy_utils.types.uuid.UUIDType(), nullable=False),
                    sa.Column('sign_id', sqlalchemy_utils.types.uuid.UUIDType(), nullable=True),
                    sa.Column('packet', common.db.data_types.Json(), nullable=False),
                    sa.Column('created_at', sa.DateTime(), nullable=False),
                    sa.ForeignKeyConstraint(['sign_id'], ['signs.id'], ondelete='CASCADE'),
                    sa.PrimaryKeyConstraint('id')
                    )
    op.create_table('rules',
                    sa.Column('number', sa.Integer(), nullable=False, autoincrement=True),
                    sa.Column('body', sa.String(), nullable=False),
                    sa.PrimaryKeyConstraint('number')
                    )
    op.create_index(op.f('ix_attack_events_created_at'), 'attack_events', ['created_at'], unique=False)
    op.create_index(op.f('ix_attack_events_sign_id'), 'attack_events', ['sign_id'], unique=False)


def downgrade():
    op.drop_index(op.f('ix_signs_to_definitions_sign_id'), table_name='signs_to_attack')
    op.drop_index(op.f('ix_signs_to_definitions_definition_id'), table_name='signs_to_attack')
    op.drop_table('signs_to_definitions')
    op.drop_index(op.f('ix_definitions_name'), table_name='definitions')
    op.drop_table('definitions')
    op.drop_table('signs')
    op.drop_index(op.f('ix_attack_events_sign_id'), table_name='attack_events')
    op.drop_index(op.f('ix_attack_events_created_at'), table_name='attack_events')
    op.drop_index(op.f('ix_attack_events_attack_id'), table_name='attack_events')
    op.drop_index(op.f('ix_attack_events_attack_definition_id'), table_name='attack_events')
    op.drop_table('attack_events')
