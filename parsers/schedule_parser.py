import re
from typing import Optional, Dict

TYPE_CODES: tuple[str, ...] = ('Inne', 'Zal', 'Zp', 'Ep', 'E', 'L', 'r', 'ć', 'w')
TYPE_PATTERN: str = '|'.join(re.escape(code) for code in TYPE_CODES)


def _clean_subject(subject: str) -> str:
    return subject.strip().rstrip('(').strip()


def _clean_token(token: str) -> str:
    return token.strip().strip('(),;:')


def _is_reference_token(token: str) -> bool:
    return bool(re.fullmatch(r'[A-Za-ząćęłńóśźżĄĆĘŁŃÓŚŹŻ]*\[\d+\]', token))


def _looks_like_room(token: str) -> bool:
    return bool(re.search(r'\d', token)) and not _is_reference_token(token)


def _parse_location(details: str) -> tuple[Optional[str], Optional[str]]:
    details = re.sub(r'\s+', ' ', details).strip().lstrip('),;:').strip()
    if not details:
        return None, None

    tokens = [_clean_token(token) for token in details.split()]
    tokens = [token for token in tokens if token and not _is_reference_token(token)]

    if not tokens:
        return None, None

    if tokens[0].lower() in {'aula', 'sala'} and len(tokens) > 1:
        room = f'{tokens[0]} {tokens[1]}'
        building = tokens[2] if len(tokens) > 2 else None
        return room, building

    if _looks_like_room(tokens[0]):
        room = tokens[0]
        building = tokens[1] if len(tokens) > 1 else None
        return room, building

    return None, tokens[0]


def parse_activity(raw: str) -> Dict[str, Optional[str]]:
    """
    Parses a raw activity string into structured data.

    Args:
        raw (str): Raw activity string (e.g., "MatE101" or "F1w314 S").

    Returns:
        Dict[str, Optional[str]]: Parsed subject, type, room, and building.
    """
    raw = re.sub(r'\s+', ' ', raw.strip())

    parenthesized_type = re.match(
        rf'^(?P<subject>.+?)\s*\(\s*(?P<type>{TYPE_PATTERN})\s*\)\s*(?P<details>.*)$',
        raw
    )
    if parenthesized_type:
        room, building = _parse_location(parenthesized_type.group('details'))
        return {
            "raw": raw,
            "subject": _clean_subject(parenthesized_type.group('subject')),
            "type": parenthesized_type.group('type'),
            "room": room,
            "building": building
        }

    separated_type = re.match(
        rf'^(?P<subject>.+?)\s+(?P<type>{TYPE_PATTERN})\s*(?P<details>.*)$',
        raw
    )
    if separated_type:
        room, building = _parse_location(separated_type.group('details'))
        return {
            "raw": raw,
            "subject": _clean_subject(separated_type.group('subject')),
            "type": separated_type.group('type'),
            "room": room,
            "building": building
        }

    for lesson_type in TYPE_CODES:
        compact_type = re.match(
            rf'^(?P<subject>.+?){re.escape(lesson_type)}(?P<details>(?:\d.*|\s+\S.*)?)$',
            raw
        )
        if compact_type:
            room, building = _parse_location(compact_type.group('details'))
            return {
                "raw": raw,
                "subject": _clean_subject(compact_type.group('subject')),
                "type": lesson_type,
                "room": room,
                "building": building
            }

    return {
        "raw": raw,
        "subject": None,
        "type": None,
        "room": None,
        "building": None
    }

def parse_block(block: str) -> str:
    """
    Converts a lesson block number to time range.

    Args:
        block (str): Block like "1-2", "3-4", etc.

    Returns:
        str: Time range (e.g., "08:00–09:35")
    """
    block = re.sub(r'\s+', '', block.strip()).replace('–', '-')
    block_map: dict[str, str] = {
        "1": "08:00–09:35",
        "1-2": "08:00–09:35",
        "2": "09:50–11:25",
        "3-4": "09:50–11:25",
        "3": "11:40–13:15",
        "5-6": "11:40–13:15",
        "4": "13:30–15:05",
        "7-8": "13:30–15:05",
        "5": "16:00–17:35",
        "9-10": "16:00–17:35",
        "6": "17:50–19:25",
        "11-12": "17:50–19:25",
        "7": "19:40–21:15",
        "13-14": "19:40–21:15"
    }

    return block_map.get(block, block)
