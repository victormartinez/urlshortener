#!/bin/bash
sleep 8
alembic upgrade head
uvicorn --host 0.0.0.0 urlshorten.main:app
