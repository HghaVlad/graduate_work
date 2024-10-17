#!/bin/bash

# transfer data from sqlite to postgres and check consistency
python sqlite_to_postgres/load_data.py

# test transfering data result
# python sqlite_to_postgres/tests/check_consistency.py