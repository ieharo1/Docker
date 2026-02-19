-- PostgreSQL initialization script for monitoring dashboard
-- This script creates required extensions and initial configuration

-- Enable useful extensions
CREATE EXTENSION IF NOT EXISTS pg_stat_statements;
CREATE EXTENSION IF NOT EXISTS pg_trgm;
CREATE EXTENSION IF NOT EXISTS btree_gin;

-- Create schema for monitoring
CREATE SCHEMA IF NOT EXISTS monitoring;

-- Set up connection limits
ALTER SYSTEM SET max_connections = 200;
ALTER SYSTEM SET shared_buffers = '256MB';
ALTER SYSTEM SET effective_cache_size = '1GB';
ALTER SYSTEM SET work_mem = '16MB';

-- Initialize with data
SELECT pg_reload_conf();

GRANT ALL PRIVILEGES ON SCHEMA monitoring TO postgres;
