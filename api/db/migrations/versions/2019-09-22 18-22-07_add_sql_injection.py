"""add_sql_injection

Revision ID: 4c752e23d09d
Revises: d3d0753d7f43
Create Date: 2019-09-22 18:22:07.173851

"""
import sqlalchemy as sa
import sqlalchemy_utils
from alembic import op
# revision identifiers, used by Alembic.
from sqlalchemy import table, column

import common

revision = '4c752e23d09d'
down_revision = 'd3d0753d7f43'
branch_labels = None
depends_on = None


def upgrade():
    seed_signs()


def downgrade():
    pass


def seed_signs():
    signs_table = table('signs',
                        column('id', sqlalchemy_utils.types.uuid.UUIDType),
                        column('packet_type', sa.String),
                        column('name', sa.String),
                        column('src', sa.Enum),
                        column('dst', sa.Enum),
                        column('checked_fields', common.db.data_types.Json),
                        column('result_criteria', sa.Enum)
                        )
    signs = [
        {
            "id": "8644851a-36b3-4a8f-be5f-afb7f82c35ca",
            "name": "sql_injection",
            "packet_type": "HTTP",
            "checked_fields": [{
                "request_uri": ".*union.*",
                "search_type": "REGEX",
            }],
            "dst": "HOME",
            "src": "EXTERNAL",
            "result_criteria": "ALL"
        },
    ]
    op.bulk_insert(signs_table, signs, multiinsert=False)
