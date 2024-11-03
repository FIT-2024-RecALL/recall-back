#!/bin/bash
docker compose up -d
docker compose exec minio bash /setup.sh
