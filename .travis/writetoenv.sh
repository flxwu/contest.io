#!/bin/bash

echo "GITHUB_CLIENT_ID=${GITHUB_CLIENT_ID}" >> .env
echo "GITHUB_CLIENT_SECRET=${GITHUB_CLIENT_SECRET}" >> .env
echo "SECRET_KEY=${SECRET_KEY}" >> .env
echo "Successfully wrote environment variables"
