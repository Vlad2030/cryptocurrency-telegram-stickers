def generate_expression(interval_seconds: int = 0) -> str:
    expression = "{} {} {} {} {}"

    if interval_seconds <= 0:
        return expression.format("*", "*", "*", "*", "*")

    total_seconds = interval_seconds
    seconds = total_seconds % 60
    total_minutes = total_seconds // 60
    minutes = total_minutes % 60
    total_hours = total_minutes // 60
    hours = total_hours % 24
    total_days = total_hours // 24
    days = total_days % 31

    return expression.format(
        ("*" if minutes == 0 else f"*/{minutes}"),
        ("*" if hours == 0 else f"*/{hours}"),
        ("*" if days < 1 else f"*/{days}"),
        ("*"),
        ("*"),
    )
