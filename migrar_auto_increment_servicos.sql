-- Script para tornar cod_servico auto-increment no PostgreSQL
-- Execute no banco com: psql -U studio_user -d estudio_fotografia -f migrar_auto_increment_servicos.sql

-- 1. Criar a sequence para auto-increment
CREATE SEQUENCE IF NOT EXISTS "DIM_SERVICOS_cod_servico_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

-- 2. Atribuir a sequence à coluna
ALTER TABLE "DIM_SERVICOS" 
    ALTER COLUMN cod_servico SET DEFAULT nextval('"DIM_SERVICOS_cod_servico_seq"'::regclass);

-- 3. Sincronizar a sequence com o maior valor existente
SELECT setval('"DIM_SERVICOS_cod_servico_seq"', 
              COALESCE((SELECT MAX(cod_servico) FROM "DIM_SERVICOS"), 0), 
              false);

-- 4. Tornar a sequence "owned" pela coluna (opcional, boa prática)
ALTER SEQUENCE "DIM_SERVICOS_cod_servico_seq" OWNED BY "DIM_SERVICOS".cod_servico;
