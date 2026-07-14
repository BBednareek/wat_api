from google.api_core.exceptions import GoogleAPIError
from google.cloud import firestore
from google.cloud.firestore_v1.field_path import FieldPath
from google.cloud.firestore_v1.base_query import FieldFilter
from pathlib import Path
from models.schedule import GroupsInDepartment
from google.oauth2 import service_account
import logging

logger = logging.getLogger(__name__)

PROJECT_ROOT = Path(__file__).resolve().parents[1]
KEY_PATH = PROJECT_ROOT / "key.json"

if not KEY_PATH.exists():
    raise RuntimeError(
        f"Nie znaleziono klucza Firebase: {KEY_PATH}"
    )

credentials = service_account.Credentials.from_service_account_file(
    str(KEY_PATH)
)
db: firestore.AsyncClient = firestore.AsyncClient()


async def get_grouped_faculty_groups(department: str) -> GroupsInDepartment:
    """
    Fetches all group names from Firestore and organizes them by faculty prefix.

    Returns:
        GroupedGroups: Dictionary where keys are faculty prefixes (e.g., 'WCY'),
                       and values are lists of group names.
    """

    prefix: str = department[:3]

    if len(prefix) < 3:
        from exceptions.schedule_exceptions import FirestoreConnectionError
        raise FirestoreConnectionError("Invalid department prefix")

    try:
        groups_collection = db.collection('groups')

        lower_bound = groups_collection.document(prefix)
        upper_bound = groups_collection.document(prefix + "\uf8ff")

        query = (
            groups_collection
            .where(
                filter=FieldFilter(
                    FieldPath.document_id(),
                    ">=",
                    lower_bound,
                )
            )
            .where(
                filter=FieldFilter(
                    FieldPath.document_id(),
                    "<=",
                    upper_bound
                )
            )
        )
        group_id = [doc.id async for doc in query.stream()]
        return GroupsInDepartment(groups_by_department=group_id)

    except GoogleAPIError as e:
        logger.exception("Firestore error: %s: %s", type(e).__name__, str(e))
        from exceptions.schedule_exceptions import FirestoreConnectionError
        raise FirestoreConnectionError("Failed to retrieve groups from Firestore.") from e
