#!/bin/bash
until curl -s $MINIO_SERVER_HOSTNAME; do
  echo "Waiting for MinIO to start..."
  sleep 5
done
mc alias set local $MINIO_SERVER_HOSTNAME $MINIO_ADMIN_LOGIN $MINIO_ADMIN_PASSWORD
mc admin user add local $MINIO_LOGIN $MINIO_PASSWORD
mc admin policy attach local readwrite --user $MINIO_LOGIN
mc mb /mnt/minio-volume/$MINIO_BUCKET_NAME
