## Plano de Deploy — Produção (Ubuntu 22.04)

---

### Arquitetura Sugerida

```
[Navegador] → [Nginx] → [Gunicorn] → [Django App] → [PostgreSQL]
                 │
                 ├── /static/ → arquivos estáticos
                 └── /media/ → uploads (contratos .docx)
```

**Servidor Web**: **Nginx** + **Gunicorn** — padrão da indústria para Django, mais leve e performático que Apache.

---

### Passo a Passo

#### 1. Atualizar o sistema e instalar dependências

```bash
# Atualizar pacotes
sudo apt update && sudo apt upgrade -y

# Instalar Python, pip, venv e ferramentas de build
sudo apt install -y python3 python3-pip python3-venv python3-dev

# Instalar PostgreSQL e bibliotecas
sudo apt install -y postgresql postgresql-client libpq-dev

# Instalar Nginx
sudo apt install -y nginx

# Instalar git
sudo apt install -y git
```

#### 2. Configurar o PostgreSQL

```bash
# Iniciar e habilitar PostgreSQL
sudo systemctl start postgresql
sudo systemctl enable postgresql

# Acessar o console do PostgreSQL
sudo -u postgres psql
```

Dentro do `psql`:

```sql
CREATE USER studio_user WITH PASSWORD 'sua_senha_aqui';
CREATE DATABASE estudio_fotografia OWNER studio_user;
GRANT ALL PRIVILEGES ON DATABASE estudio_fotografia TO studio_user;
\q
```

#### 3. Criar usuário do sistema e estrutura de diretórios

```bash
# Criar usuário para rodar a aplicação (sem shell de login)
sudo adduser --system --group --no-create-home studioapp

# Criar diretório da aplicação
sudo mkdir -p /var/www/studio
sudo chown studioapp:studioapp /var/www/studio
```

#### 4. Clonar o repositório e configurar ambiente Python

```bash
# Clonar o projeto
cd /var/www/studio
sudo -u studioapp git clone <URL_DO_REPOSITORIO> .

# Criar virtualenv
sudo -u studioapp python3 -m venv .venv

# Ativar e instalar dependências
sudo -u studioapp bash -c "source .venv/bin/activate && pip install --upgrade pip && pip install -r requirements.txt"

# Instalar Gunicorn
sudo -u studioapp bash -c "source .venv/bin/activate && pip install gunicorn"
```

#### 5. Configurar variáveis de ambiente e settings de produção

Criar arquivo `/var/www/studio/.env`:

```bash
sudo -u studioapp nano /var/www/studio/.env
```

Conteúdo:

```
DJANGO_SECRET_KEY=gerar_nova_chave_aqui
DJANGO_DEBUG=False
DJANGO_ALLOWED_HOSTS=seudominio.com,www.seudominio.com
DB_NAME=estudio_fotografia
DB_USER=studio_user
DB_PASSWORD=sua_senha_aqui
DB_HOST=localhost
DB_PORT=5432
```

Criar `/var/www/studio/studio/settings_prod.py` (ou modificar `settings.py` para ler variáveis de ambiente):

```python
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.environ['DJANGO_SECRET_KEY']
DEBUG = os.environ.get('DJANGO_DEBUG', 'False') == 'True'
ALLOWED_HOSTS = os.environ.get('DJANGO_ALLOWED_HOSTS', '').split(',')

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ['DB_NAME'],
        'USER': os.environ['DB_USER'],
        'PASSWORD': os.environ['DB_PASSWORD'],
        'HOST': os.environ.get('DB_HOST', 'localhost'),
        'PORT': os.environ.get('DB_PORT', '5432'),
    }
}

STATIC_ROOT = BASE_DIR / 'staticfiles'
MEDIA_ROOT = BASE_DIR / 'media'

# Segurança adicional em produção
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True
SECURE_SSL_REDIRECT = True
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
X_FRAME_OPTIONS = 'DENY'
```

#### 6. Rodar migrações e assets estáticos

```bash
cd /var/www/studio
sudo -u studioapp bash -c "source .venv/bin/activate && python manage.py migrate --settings=studio.settings_prod"
sudo -u studioapp bash -c "source .venv/bin/activate && python manage.py collectstatic --noinput --settings=studio.settings_prod"
sudo -u studioapp bash -c "source .venv/bin/activate && python manage.py createsuperuser --settings=studio.settings_prod"
```

#### 7. Criar diretório para templates de contrato

```bash
sudo -u studioapp mkdir -p /var/www/studio/templates_contratos
sudo -u studioapp mkdir -p /var/www/studio/media/contratos
```

#### 8. Configurar Gunicorn como serviço systemd

Criar arquivo `/etc/systemd/system/studioapp.service`:

```ini
[Unit]
Description=Gunicorn - StudioApp Django
After=network.target postgresql.service

[Service]
Type=exec
User=studioapp
Group=studioapp
WorkingDirectory=/var/www/studio
EnvironmentFile=/var/www/studio/.env
ExecStart=/var/www/studio/.venv/bin/gunicorn studio.wsgi:application \
    --bind unix:/var/www/studio/studioapp.sock \
    --workers 3 \
    --timeout 120 \
    --access-logfile /var/log/studioapp/access.log \
    --error-logfile /var/log/studioapp/error.log
Restart=always

[Install]
WantedBy=multi-user.target
```

```bash
# Criar diretório de logs
sudo mkdir -p /var/log/studioapp
sudo chown studioapp:studioapp /var/log/studioapp

# Ativar e iniciar o serviço
sudo systemctl daemon-reload
sudo systemctl enable studioapp
sudo systemctl start studioapp
sudo systemctl status studioapp
```

#### 9. Configurar Nginx como proxy reverso

Criar arquivo `/etc/nginx/sites-available/studioapp`:

```nginx
server {
    listen 80;
    server_name seudominio.com www.seudominio.com;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl;
    server_name seudominio.com www.seudominio.com;

    ssl_certificate /etc/letsencrypt/live/seudominio.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/seudominio.com/privkey.pem;

    client_max_body_size 20M;

    location /static/ {
        alias /var/www/studio/staticfiles/;
        expires 30d;
        add_header Cache-Control "public, immutable";
    }

    location /media/ {
        alias /var/www/studio/media/;
        expires 7d;
    }

    location / {
        proxy_pass http://unix:/var/www/studio/studioapp.sock;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

**Alternativa sem SSL (intranet/local):**

```nginx
server {
    listen 80;
    server_name 192.168.x.x ou localhost;

    client_max_body_size 20M;

    location /static/ {
        alias /var/www/studio/staticfiles/;
    }

    location /media/ {
        alias /var/www/studio/media/;
    }

    location / {
        proxy_pass http://unix:/var/www/studio/studioapp.sock;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

Ativar:

```bash
sudo ln -s /etc/nginx/sites-available/studioapp /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

#### 10. (Opcional) Configurar SSL com Let's Encrypt

```bash
sudo apt install -y certbot python3-certbot-nginx
sudo certbot --nginx -d seudominio.com -d www.seudominio.com
```

#### 11. Ajustar permissões

```bash
sudo chown -R studioapp:www-data /var/www/studio/media
sudo chown -R studioapp:www-data /var/www/studio/templates_contratos
sudo chmod -R 755 /var/www/studio/media
sudo chmod -R 755 /var/www/studio/templates_contratos
```

#### 12. Firewall (se ativo)

```bash
sudo ufw allow 22/tcp        # SSH
sudo ufw allow 80/tcp        # HTTP
sudo ufw allow 443/tcp       # HTTPS
sudo ufw enable
```

---

### Estrutura final de diretórios

```
/var/www/studio/
├── .venv/                    # Virtualenv
├── .env                      # Variáveis de ambiente
├── apps/                     # Código fonte
├── studio/                   # Settings, urls, wsgi
├── templates/                # Templates Django
├── static/                   # CSS, JS (desenvolvimento)
├── staticfiles/              # Coletados (produção)
├── media/contratos/          # Uploads
├── templates_contratos/      # Templates .docx
└── studioapp.sock            # Socket do Gunicorn
```

---

### Comandos úteis para manutenção

```bash
# Ver logs do Gunicorn
sudo journalctl -u studioapp -f

# Ver logs do Nginx
sudo tail -f /var/log/nginx/access.log
sudo tail -f /var/log/nginx/error.log

# Reiniciar após deploy
sudo systemctl restart studioapp
sudo systemctl reload nginx

# Atualizar código (via git pull)
cd /var/www/studio
sudo -u studioapp git pull
sudo -u studioapp bash -c "source .venv/bin/activate && pip install -r requirements.txt"
sudo -u studioapp bash -c "source .venv/bin/activate && python manage.py migrate"
sudo -u studioapp bash -c "source .venv/bin/activate && python manage.py collectstatic --noinput"
sudo systemctl restart studioapp
```

---

### Perguntas para você:

| Pergunta | Para definir |
|---|---|
| **Domínio/IP** | O app será acessado via domínio público ou IP local da rede? |
| **SSL** | Precisa de HTTPS (certificado Let's Encrypt) ou é uso interno? |
| **Nº de funcionários** | Para dimensionar workers do Gunicorn (regra: `2-4 × CORES`) |
| **Banco existente?** | O banco de produção já tem dados ou começa vazio? |
| **Backup** | Precisa de plano de backup do banco (pg_dump via cron)? |

Quer que eu ajuste algo no plano ou pode seguir com a implementação?

---

