#!/bin/bash
echo "=== Iniciando Gestao de Estudio de Fotografia ==="

PROJECT_DIR="/mnt/d/Arquivos Pessoais/Diversos/SISTEMAS/Novo APP Estudio/GestaoEstudioFotografia"

cd "$PROJECT_DIR" || { echo "Diretorio nao encontrado"; exit 1; }

source .venv/bin/activate

if ! command -v psql &> /dev/null; then
    echo "AVISO: PostgreSQL nao encontrado. Instale com: sudo apt install postgresql postgresql-contrib libpq-dev"
fi

IP=$(ip addr show | grep -oP '(?<=inet\s)\d+\.\d+\.\d+\.\d+' | grep -v '127.0.0.1' | head -1)

echo ""
echo "========================================"
echo "  Servidor iniciado!"
echo "  Acessar local:  http://localhost:8000"
if [ -n "$IP" ]; then
    echo "  Rede local:    http://$IP:8000"
fi
echo "  Admin:          http://localhost:8000/admin/"
echo "========================================"
echo ""

python manage.py runserver 0.0.0.0:8000
