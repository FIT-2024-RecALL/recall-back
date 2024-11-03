#!/bin/bash
docker compose up -d
docker compose exec minio /setup.sh