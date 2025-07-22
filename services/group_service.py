from google.cloud import firestore
from collections import defaultdict
from os import environ
from google.cloud.firestore_v1 import DocumentSnapshot
from models.schedule import GroupedGroups


environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'key.json'
db: firestore.Client = firestore.Client()


async def get_grouped_faculty_groups() -> GroupedGroups:
    """
    Fetches all group names from Firestore and organizes them by faculty prefix.

    Returns:
        GroupedGroups: Dictionary where keys are faculty prefixes (e.g., 'WCY'),
                       and values are lists of group names.
    """
    try:
        groups_ref = db.collection("groups").list_documents()
        grouped: dict[str, list[str]] = defaultdict(list)

        docs: list[DocumentSnapshot] = []
        for group in groups_ref:
            docs.append(group)

        for doc in docs:
            group_name: str = doc.id
            faculty: str = group_name[:3].upper()
            grouped[faculty].append(group_name)

        return GroupedGroups(groups_by_faculty = dict(grouped))

    except Exception as e:
        from exceptions.schedule_exceptions import FirestoreConnectionError
        raise FirestoreConnectionError("Failed to retrieve groups from Firestore.") from e
