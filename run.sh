#!/usr/bin/env bash
set -o errexit

uv run waitress-serve --port="${PORT:-10000}" config.wsgi:application
