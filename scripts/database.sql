-- Tabla principal para transcripciones
CREATE TABLE IF NOT EXISTS voice_transcriptions (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    text TEXT NOT NULL,
    status VARCHAR(50) DEFAULT 'pending',
    created_at TIMESTAMPTZ DEFAULT NOW(),
    audio_url TEXT,
    metadata JSONB
);

-- Índices para optimización
CREATE INDEX idx_transcription_status ON voice_transcriptions (status);
CREATE INDEX idx_transcription_created ON voice_transcriptions (created_at);