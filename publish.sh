#!/bin/bash

set -e

VERSION="${1:?Usage: ./publish.sh <version> [gh-options]}"
shift || true

ARCHIVE="/tmp/PZ_Translation_Schemas.zip"
zip -r "$ARCHIVE" PZ_Translation_Schemas settings.json

gh release create "$VERSION" "$ARCHIVE" \
  --notes "Game version: $VERSION" \
  "$@"

rm -f "$ARCHIVE"
