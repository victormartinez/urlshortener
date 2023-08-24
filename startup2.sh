#!/bin/bash
sleep 5
uvicorn --host 0.0.0.0 urlshorten.main:app
