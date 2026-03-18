-- ============================================
-- Indian MSME Compliance RAG Bot — Supabase Schema
-- Run this in your Supabase SQL Editor
-- ============================================

-- 1. Enable pgvector extension
CREATE EXTENSION IF NOT EXISTS vector;

-- 2. RESET TABLE (Required to change vector dimension to 384)
DROP TABLE IF EXISTS documents CASCADE;

-- 3. Create documents table (384 dimensions for all-MiniLM-L6-v2)
CREATE TABLE IF NOT EXISTS documents (
    id BIGSERIAL PRIMARY KEY,
    content TEXT NOT NULL,
    metadata JSONB DEFAULT '{}'::JSONB,
    embedding VECTOR(384),  -- HuggingFace all-MiniLM-L6-v2 dimension
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- 3. Create index for fast similarity search
-- Re-enabling ivfflat since we are now at 384 dimensions (below the 2000 limit)
CREATE INDEX IF NOT EXISTS documents_embedding_idx
ON documents
USING ivfflat (embedding vector_cosine_ops)
WITH (lists = 100);

-- 4. Create match_documents_v4 function
CREATE OR REPLACE FUNCTION match_documents_v4(
    query_embedding VECTOR(384),
    match_threshold FLOAT DEFAULT 0.5,
    match_count INT DEFAULT 5
)
RETURNS TABLE (
    id BIGINT,
    content TEXT,
    metadata JSONB,
    similarity FLOAT
)
LANGUAGE sql STABLE
AS $$
    SELECT
        documents.id,
        documents.content,
        documents.metadata,
        1 - (documents.embedding <=> query_embedding) AS similarity
    FROM documents
    WHERE 1 - (documents.embedding <=> query_embedding) > match_threshold
    ORDER BY documents.embedding <=> query_embedding
    LIMIT match_count;
$$;

-- 5. Enable Row Level Security (optional, for production)
-- ALTER TABLE documents ENABLE ROW LEVEL SECURITY;
-- CREATE POLICY "Allow public read" ON documents FOR SELECT USING (true);
-- CREATE POLICY "Allow authenticated insert" ON documents FOR INSERT WITH CHECK (true);
