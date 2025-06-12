from google.cloud import firestore
from typing import Any
from os import getenv, path

from app.services.error_handler import handle_errors

def get_firestore_client() -> firestore.Client:
    """Initializes and returns a Firestore client."""
    credentials_path = getenv("GOOGLE_APPLICATION_CREDENTIALS")
    if credentials_path and not path.isfile(credentials_path):
        raise RuntimeError(f"Invalid credentials path: {credentials_path}")
    return firestore.Client(credentials=credentials_path)

client = get_firestore_client()

@handle_errors
def get_schedule(doc_id: str) -> dict[str, Any] | None:
    """Fetch a schedule by document ID."""
    doc_ref = client.collection("schedules").document(doc_id)
    doc = doc_ref.get()
    return doc.to_dict() if doc.exists else None


@handle_errors
def list_schedules() -> list[dict[str, Any]]:
    """List all faculty groups."""
    return [doc.to_dict() for doc in client.collection("schedules").stream()]
