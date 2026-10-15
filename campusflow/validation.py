"""Pure validation helpers: no input(), no print(), no mutation."""

ALLOWED_CATEGORIES = ("Network", "Hardware", "Software", "Other")
ALLOWED_URGENCIES = ("low", "medium", "high")
ALLOWED_STATUSES = ("open", "in_progress", "resolved")
ALLOWED_PRIORITIES = ("critical", "high", "medium", "low")


class ValidationError(ValueError):
    """Raised when data breaks a CampusFlow rule."""


def check_title(title):
    if not isinstance(title, str):
        raise ValidationError("Title must be text")
    cleaned = title.strip()
    if not cleaned:
        raise ValidationError("Title must not be blank")
    return cleaned


def check_category(category):
    if not isinstance(category, str):
        raise ValidationError("Category must be text")
    cleaned = category.strip().casefold()
    for allowed in ALLOWED_CATEGORIES:
        if allowed.casefold() == cleaned:
            return allowed
    raise ValidationError(
        f"Category must be one of: {', '.join(ALLOWED_CATEGORIES)}"
    )


def check_urgency(urgency):
    if not isinstance(urgency, str):
        raise ValidationError("Urgency must be text")
    cleaned = urgency.strip().casefold()
    if cleaned not in ALLOWED_URGENCIES:
        raise ValidationError(
            f"Urgency must be one of: {', '.join(ALLOWED_URGENCIES)}"
        )
    return cleaned


def check_affected_users(value):
    # type(...) is int, not isinstance, because isinstance(True, int) is True
    if type(value) is not int:
        raise ValidationError("Affected users must be a whole number")
    if value <= 0:
        raise ValidationError("Affected users must be greater than 0")
    return value


def check_staff_name(name):
    if not isinstance(name, str) or not name.strip():
        raise ValidationError("Staff name cannot be empty")
    return name.strip()


NOTE_MIN_LENGTH = 5
NOTE_MAX_LENGTH = 300


def check_note_author(author):
    if not isinstance(author, str) or not author.strip():
        raise ValidationError("Note author cannot be empty")
    return author.strip()


def check_note_message(message):
    if not isinstance(message, str):
        raise ValidationError("Note message must be text")
    cleaned = message.strip()
    if not NOTE_MIN_LENGTH <= len(cleaned) <= NOTE_MAX_LENGTH:
        raise ValidationError(
            f"Note message must be {NOTE_MIN_LENGTH}-{NOTE_MAX_LENGTH} "
            f"characters (got {len(cleaned)})"
        )
    return cleaned