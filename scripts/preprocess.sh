#!/bin/sh

# First combine dfdc & casual conversations metadata
python merge-metadata.py --di dfdc_metadata.json --ci correspondences.json --o metadata-merged.json

# Sanitize dataset and metadata
python sanitize-data.py --f metadata-merged.json --o metadata-sanitized.json

# Optional print data statistics after sanitizing
python get-data-statistics.py --f metadata-sanitized.json

# Prepare train/test splits
python prepare-splits.py --f metadata-sanitized.json --tp 80