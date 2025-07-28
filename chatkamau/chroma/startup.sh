#!/bin/bash

echo "Starting Chroma vector database..."
chroma run --host localhost --port 8000 --path ./chroma_data
