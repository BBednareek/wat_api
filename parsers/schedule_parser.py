import re
from typing import Optional, Dict

def parse_activity(raw: str) -> Dict[str, Optional[str]]:
    """
    Parses a raw activity string into structured data.

    Args:
        raw (str): Raw activity string (e.g., "MatE101" or "F1w314 S").

    Returns:
        Dict[str, Optional[str]]: Parsed subject, type, room, and building.
    """
    raw = raw.strip()
    parts = raw.split()

    building: Optional[str] = None
    if len(parts) == 2:
        raw, building = parts[0], parts[1]

    type_codes: list[str] = ['Ep', 'E', 'L', 'r', 'ć', 'w', 'Zp', 'Zal', 'Inne']
    type_pattern: str = '|'.join(type_codes)

    patterns = [
        rf'^([A-Za-z0-9]+?)({type_pattern})(\d+)$',
        rf'^([A-Za-z0-9]+?)({type_pattern})([A-Za-z0-9]+)$',
        rf'^([A-Za-z0-9]+?)({type_pattern})$',
        rf'^(.+?)({type_pattern})(.+)$'
    ]

    for pattern in patterns:
        match = re.match(pattern, raw)
        if match:
            subject, lesson_type, *rest = match.groups()
            room = rest[0].strip() if rest else None
            return {
                "raw": raw + (f" {building}" if building else ""),
                "subject": subject.strip(),
                "type": lesson_type,
                "room": room,
                "building": building
            }

    return {
        "raw": raw,
        "subject": None,
        "type": None,
        "room": None,
        "building": building
    }

def parse_block(block: str) -> str:
    """
    Converts a lesson block number to time range.

    Args:
        block (str): Block like "1-2", "3-4", etc.

    Returns:
        str: Time range (e.g., "08:00–09:35")
    """
    block_map = {
        "1-2": "08:00–09:35",
        "3-4": "09:50–11:25",
        "5-6": "11:40–13:15",
        "7-8": "13:30–15:05",
        "9-10": "16:00–17:35",
        "11-12": "17:50–19:25",
        "13-14": "19:40–21:15"
    }
    return block_map.get(block, block)
