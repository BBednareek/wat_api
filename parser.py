import re

def parse_activity(raw: str):
    raw: str = raw.strip()
    parts: list[str] = raw.split()

    building = None
    if len(parts) == 2:
        raw, building = parts[0], parts[1]

    type_codes: list[str] = ['Ep', 'E', 'L', 'r', 'ć', 'w']
    type_pattern: str = '|'.join(type_codes)

    match = re.match(rf'^([A-Za-z0-9]+?)({type_pattern})(\d+)$', raw)
    if match:
        subject, lesson_type, room = match.groups()
        return {
            "raw": raw + (f" {building}" if building else ""),
            "subject": subject,
            "type": lesson_type,
            "room": room,
            "building": building
        }

    match = re.match(rf'^([A-Za-z0-9]+?)({type_pattern})([A-Za-z0-9]+)$', raw)
    if match:
        subject, lesson_type, room = match.groups()
        return {
            "raw": raw + (f" {building}" if building else ""),
            "subject": subject,
            "type": lesson_type,
            "room": room,
            "building": building
        }

    match = re.match(rf'^([A-Za-z0-9]+?)({type_pattern})$', raw)
    if match:
        subject, lesson_type = match.groups()
        return {
            "raw": raw + (f" {building}" if building else ""),
            "subject": subject,
            "type": lesson_type,
            "room": None,
            "building": building
        }

    match = re.match(rf'^(.+?)({type_pattern})(.+)$', raw)
    if match:
        subject, lesson_type, room = match.groups()
        return {
            "raw": raw + (f" {building}" if building else ""),
            "subject": subject.strip(),
            "type": lesson_type,
            "room": room.strip(),
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
    block_map = {
        "1-2": "08:00–09:35",
        "3-4": "09:50–11:25",
        "5-6": "11:40–13:15",
        "7-8": "13:30–15:05",
        "9-10": "16:00-17:35",
        "11-12": "17:50-19:25",
        "13-14": "19:40–21:15"
    }
    return block_map.get(block, block)
