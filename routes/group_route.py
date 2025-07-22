from fastapi import APIRouter

from models.schedule import GroupedGroups
from services.group_service import get_grouped_faculty_groups

router: APIRouter = APIRouter(prefix = '/groups', tags = ['Groups'])

@router.get("/faculty", response_model = GroupedGroups)
async def grouped_groups():
    """
        Returns all academic groups grouped by faculty prefix.

        Returns:
            GroupedGroups (dict[str, list[str]]): Mapping of faculty prefixes to group names.
        """
    return await get_grouped_faculty_groups()