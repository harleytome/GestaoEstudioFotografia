#!/bin/bash
echo "=== Parando servidor ==="
pkill -f "manage.py runserver" 2>/dev/null && echo "Servidor parado." || echo "Nenhum servidor em execucao."
