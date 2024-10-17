#!/bin/bash

# Apply migrations
alembic upgrade head

# Create partition tables
# psql -U app -d auth_database -f alembic/create_partition_table_entry_histories.ddl

# Start service
python -m uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload
