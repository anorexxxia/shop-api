
#!/bin/bash
set -euo pipefail

psql \
  -v ON_ERROR_STOP=1 \
  --username "$POSTGRES_USER" \
  --dbname "$POSTGRES_DB" \
  --set=db_owner="$POSTGRES_USER" \
  --set=shop_db="$POSTGRES_DB" \
  --set=readonly_user="$READONLY_DB_USER" \
  --set=readonly_password="$READONLY_DB_PASSWORD" <<'SQL'
CREATE DATABASE grpc_auth OWNER :"db_owner";

CREATE ROLE :"readonly_user"
    LOGIN PASSWORD :'readonly_password';

GRANT CONNECT ON DATABASE :"shop_db" TO :"readonly_user";
GRANT USAGE ON SCHEMA public TO :"readonly_user";

ALTER DEFAULT PRIVILEGES
    FOR ROLE :"db_owner"
    IN SCHEMA public
    GRANT SELECT ON TABLES TO :"readonly_user";
SQL
