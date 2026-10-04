#!/bin/bash
set -xe

cd `dirname $0`

uv run python -m unittest tests.test_interpreters -vf
#uv run python -m unittest tests.test_compilers -vf

ruff format
ruff check
