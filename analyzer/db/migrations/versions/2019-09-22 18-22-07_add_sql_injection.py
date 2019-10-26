"""add_sql_injection

Revision ID: 4c752e23d09d
Revises: d3d0753d7f43
Create Date: 2019-09-22 18:22:07.173851

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
from sqlalchemy import table, column

import analyzer

revision = '4c752e23d09d'
down_revision = 'd3d0753d7f43'
branch_labels = None
depends_on = None


def upgrade():
    seed_signs()
    seed_attacks()
    seed_relations()


def downgrade():
    pass


def seed_attacks():
    attack_definitions_table = table('attack_definitions',
                                     column('id', analyzer.db.data_types.UUID),
                                     column('name', sa.String),
                                     column('description', sa.String),
                                     column('criterion', sa.Enum),
                                     )
    attack_definitions = [
        {
            "id": "e5366286-e3b0-45b3-9d09-75fa69ae5a4d",
            "name": "sql_injection",
            "description": "SQL injection",
            "criterion": "ALL"
        }
    ]
    op.bulk_insert(attack_definitions_table, attack_definitions, multiinsert=False)


def seed_signs():
    signs_table = table('signs',
                        column('id', analyzer.db.data_types.UUID),
                        column('packet_type', sa.String),
                        column('order', sa.INTEGER),
                        column('search_type', sa.Enum),
                        column('src', sa.Enum),
                        column('dst', sa.Enum),
                        column('checked_fields', analyzer.db.data_types.Json),
                        column('result_criteria', sa.Enum),
                        column('search_pattern_id', analyzer.db.data_types.UUID),
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
    relation_table = table('signs_to_attack',
                           column('sign_id', analyzer.db.data_types.UUID),
                           column('attack_definition_id', analyzer.db.data_types.UUID),
                           )
    relations = [
        {
            "sign_id": "8644851a-36b3-4a8f-be5f-afb7f82c35ca",
            "attack_definition_id": "e5366286-e3b0-45b3-9d09-75fa69ae5a4d",
        },
        {
            "sign_id": "8fae99ea-b1a1-43b0-9832-5740391eab92",
            "attack_definition_id": "e5366286-e3b0-45b3-9d09-75fa69ae5a4d",
        }
    ]
    op.bulk_insert(relation_table, relations, multiinsert=False)
