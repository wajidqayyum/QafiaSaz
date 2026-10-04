import sqlite3
import re
from fastapi import FastAPI, Query, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional
from pydantic import BaseModel

app = FastAPI(title="QafiaSaz API", description="High-performance backend for Urdu/Arabic Rhymes (Qafiya) and Meter (Aruuz)")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

import os

# Resolve DB path dynamically for Vercel Serverless environment
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, 'qafiya.db')

def get_db_connection():
    # Adding 'uri=True' and 'mode=ro' is a good practice for serverless to enforce read-only
    conn = sqlite3.connect(f"file:{DB_PATH}?mode=ro", uri=True, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn

class WordResponse(BaseModel):
    id: int
    word: str
    meter: str
    source: str

def normalize_to_numeric(m: str) -> str:
    # Convert various formats to numeric (2, 1)
    # Symbolic to numeric
    m = m.replace("=", "2").replace("-", "1").replace("x", "1")
    # Real App Mnemonic mapping: د = 2, ا = 1
    m = m.replace("د", "2").replace("ا", "1")
    # Clean any other spaces
    m = m.replace(" ", "")
    # Remove any non-numeric characters left over to avoid errors
    m = ''.join(c for c in m if c in '12')
    return m

def normalize_to_symbolic(m: str) -> str:
    num = normalize_to_numeric(m)
    return num.replace("2", "=").replace("1", "-")

@app.get("/api/rhyme", response_model=List[WordResponse])
def get_rhymes(
    suffix: str = Query(..., description="The ending characters to rhyme with, e.g., 'ار'"),
    meter: Optional[str] = Query(None, description="Optional meter to filter by, e.g., '21' or '=-' or 'داد'")
):
    """
    Get words that end with the given suffix, optionally filtered by exact meter.
    Uses reversed word index for instantaneous lookups.
    """
    if not suffix:
        raise HTTPException(status_code=400, detail="Suffix cannot be empty")
        
    reversed_suffix = suffix[::-1]
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    if meter:
        num_meter = normalize_to_numeric(meter)
        sym_meter = normalize_to_symbolic(meter)
        
        # Match exactly for numeric and symbolic formats to avoid confusing prefix results
        query = '''
            SELECT id, word, meter, source FROM words 
            WHERE word_reverse LIKE ? AND (meter = ? OR meter = ?) 
        '''
        cursor.execute(query, (reversed_suffix + '%', num_meter, sym_meter))
    else:
        query = "SELECT id, word, meter, source FROM words WHERE word_reverse LIKE ?"
        cursor.execute(query, (reversed_suffix + '%',))
    
    results = cursor.fetchall()
    conn.close()
    
    return [WordResponse(id=row["id"], word=row["word"], meter=row["meter"], source=row["source"]) for row in results]

@app.get("/api/meter", response_model=List[WordResponse])
def get_by_meter(meter: str = Query(..., description="The taqti meter code, e.g., '212'")):
    conn = get_db_connection()
    cursor = conn.cursor()
    num_meter = normalize_to_numeric(meter)
    sym_meter = normalize_to_symbolic(meter)
    query = "SELECT id, word, meter, source FROM words WHERE (meter = ? OR meter = ?)"
    cursor.execute(query, (num_meter, sym_meter))
    results = cursor.fetchall()
    conn.close()
    return [WordResponse(id=row["id"], word=row["word"], meter=row["meter"], source=row["source"]) for row in results]

@app.get("/health")
def health_check():
    return {"status": "ok"}
