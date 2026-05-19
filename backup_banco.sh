#!/bin/bash
# Backup do banco estudio_fotografia
# Uso: ./backup_banco.sh
# Agendar no cron: 0 3 * * * /caminho/para/backup_banco.sh

set -euo pipefail

DB_NAME="estudio_fotografia"
DB_USER="studio_user"
DB_PASSWORD="sua_senha_aqui"
BACKUP_DIR="/var/backups/postgresql"
LOG_FILE="/var/log/backup_banco.log"
DATE=$(date +%Y%m%d_%H%M)
WEEKDAY=$(date +%u)
DAY=$(date +%d)
RETENTION_DAYS=7
RETENTION_WEEKS=4

export PGPASSWORD="$DB_PASSWORD"

mkdir -p "$BACKUP_DIR/diario" "$BACKUP_DIR/semanal" "$BACKUP_DIR/mensal"

pg_dump -U "$DB_USER" -h localhost "$DB_NAME" \
    --no-owner --no-acl \
    --file="$BACKUP_DIR/diario/${DB_NAME}_${DATE}.sql"

gzip "$BACKUP_DIR/diario/${DB_NAME}_${DATE}.sql"

echo "[$(date '+%Y-%m-%d %H:%M:%S')] Backup diario concluido: ${DB_NAME}_${DATE}.sql.gz" >> "$LOG_FILE"

# Semanal (domingo)
if [ "$WEEKDAY" = "7" ]; then
    cp "$BACKUP_DIR/diario/${DB_NAME}_${DATE}.sql.gz" \
       "$BACKUP_DIR/semanal/${DB_NAME}_semana$(date +%V).sql.gz"
    find "$BACKUP_DIR/semanal" -name "*.sql.gz" -type f | sort -r | tail -n +$((RETENTION_WEEKS + 1)) | xargs -r rm
fi

# Mensal (dia 1)
if [ "$DAY" = "01" ]; then
    cp "$BACKUP_DIR/diario/${DB_NAME}_${DATE}.sql.gz" \
       "$BACKUP_DIR/mensal/${DB_NAME}_$(date +%Y%m).sql.gz"
    find "$BACKUP_DIR/mensal" -name "*.sql.gz" -type f -mtime +365 -delete
fi

find "$BACKUP_DIR/diario" -name "*.sql.gz" -type f -mtime +$RETENTION_DAYS -delete

echo "[$(date '+%Y-%m-%d %H:%M:%S')] Rotacao concluida." >> "$LOG_FILE"
