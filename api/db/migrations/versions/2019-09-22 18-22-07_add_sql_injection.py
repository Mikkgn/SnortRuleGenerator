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
    seed_definitions()
    seed_relations()


def downgrade():
    pass


def seed_definitions():
    definitions_table = table('definitions',
                              column('id', sqlalchemy_utils.types.uuid.UUIDType),
                              column('name', sa.String),
                              column('description', sa.String),
                              column('criterion', sa.Enum),
                              )
    definitions = [
        {
            "id": "e5366286-e3b0-45b3-9d09-75fa69ae5a4d",
            "name": "sql_injection",
            "description": "SQL injection",
            "criterion": "ALL"
        }
    ]
    op.bulk_insert(definitions_table, definitions, multiinsert=False)


def seed_signs():
    signs_table = table('signs',
                        column('id', sqlalchemy_utils.types.uuid.UUIDType),
                        column('packet_type', sa.String),
                        column('order', sa.INTEGER),
                        column('search_type', sa.Enum),
                        column('src', sa.Enum),
                        column('dst', sa.Enum),
                        column('checked_fields', common.db.data_types.Json),
                        column('result_criteria', sa.Enum)
                        )
    signs = [
        {
            "id": "8644851a-36b3-4a8f-be5f-afb7f82c35ca",
            "packet_type": "HTTP",
            "checked_fields": {
                "request_uri": ".*union.*"
            },
            "dst": "HOME",
            "src": "EXTERNAL",
            "order": 0,
            "search_type": "REGEX",
            "result_criteria": "ALL"
        },
        {
            "id": "8fae99ea-b1a1-43b0-9832-5740391eab92",
            "packet_type": "HTTP",
            "order": 1,
            "src": "HOME",
            "dst": "EXTERNAL",
            "checked_fields": {
                "response_code": 200
            },
            "search_type": "FULL_MATCH",
            "result_criteria": "ALL"
        }
    ]
    op.bulk_insert(signs_table, signs, multiinsert=False)


def seed_relations():
    relation_table = table('signs_to_definitions',
                           column('sign_id', sqlalchemy_utils.types.uuid.UUIDType),
                           column('definition_id', sqlalchemy_utils.types.uuid.UUIDType),
                           )
    relations = [
        {
            "sign_id": "8644851a-36b3-4a8f-be5f-afb7f82c35ca",
            "definition_id": "e5366286-e3b0-45b3-9d09-75fa69ae5a4d",
        },
        {
            "sign_id": "8fae99ea-b1a1-43b0-9832-5740391eab92",
            "definition_id": "e5366286-e3b0-45b3-9d09-75fa69ae5a4d",
        }
    ]
    op.bulk_insert(relation_table, relations, multiinsert=False)
