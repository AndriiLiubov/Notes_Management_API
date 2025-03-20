from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
import pandas as pd
from collections import Counter
import nltk
from src.database.db import get_db
from src.repository import analytics
import ssl

ssl._create_default_https_context = ssl._create_unverified_context 

nltk.download('stopwords')
from nltk.corpus import stopwords

router = APIRouter(prefix="/analytics", tags=["Analytics"])

@router.get("/")
def analyze_notes(db: Session = Depends(get_db)):
    notes = analytics.get_all_notes(db)

    notes_data = [{
    "created_at": note.created_at,
    "id": note.id,
    "title": note.title,
    "content": note.content,
    "updated_at": note.updated_at
    } for note in notes]

    # Create DataFrame
    df = pd.DataFrame(notes_data)

    # total word count across all notes,
    total_word_count = df['content'].apply(lambda x: len(x.split())).sum()

    # average note length
    average_note_length = df['content'].apply(lambda x: len(x.split())).mean()

    # most common words or phrases,
    all_words = " ".join(df['content']).split()
    stop_words = set(stopwords.words('english'))
    words = [word.lower() for word in all_words if word.lower() not in stop_words]
    word_counts = Counter(words)
    most_common_words = word_counts.most_common(10)

    # top 3 shortest notes.
    df['length'] = df['content'].apply(lambda x: len(x.split()))
    top_3_longest_notes = df.nlargest(3, 'length')[['id', 'title', 'length']]
    top_3_shortest_notes = df.nsmallest(3, 'length')[['id', 'title', 'length']]

    # collect all on one result
    stats = {
        "total_word_count": int(total_word_count),
        "average_note_length": float(average_note_length),
        "most_common_words": most_common_words,
        "top_3_longest_notes": top_3_longest_notes.to_dict(orient='records'),
        "top_3_shortest_notes": top_3_shortest_notes.to_dict(orient='records')
    }

    return stats
