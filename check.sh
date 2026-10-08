#!/bin/bash
set -xe

cd `dirname $0`

uv run python -m unittest tests.test_interpreters -vf

ruff format --exclude '*.ipynb'
ruff check --exclude '*.ipynb'
