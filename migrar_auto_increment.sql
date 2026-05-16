-- Script para tornar cod_cliente auto-increment no PostgreSQL
-- Execute no banco com: psql -U studio_user -d estudio_fotografia -f migrar_auto_increment.sql

-- 1. Criar a sequence para auto-increment
CREATE SEQUENCE IF NOT EXISTS "DIM_CLIENTES_cod_cliente_seq"
    START WITH 607
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

-- 2. Atribuir a sequence à coluna
ALTER TABLE "DIM_CLIENTES" 
    ALTER COLUMN cod_cliente SET DEFAULT nextval('"DIM_CLIENTES_cod_cliente_seq"'::regclass);

-- 3. Sincronizar a sequence com o maior valor existente
SELECT setval('"DIM_CLIENTES_cod_cliente_seq"', 
              COALESCE((SELECT MAX(cod_cliente) FROM "DIM_CLIENTES"), 0) + 1, 
              false);

-- 4. Tornar a sequence "owned" pela coluna (opcional, boa prática)
ALTER SEQUENCE "DIM_CLIENTES_cod_cliente_seq" OWNED BY "DIM_CLIENTES".cod_cliente;
