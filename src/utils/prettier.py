import datetime
import typing

number: typing.TypeAlias = int | float


def price_indented(value: number, quote_symbol: str) -> str:
    # wtf lol
    decimal = f"{abs(value):.15f}".rstrip("0").split(".")[1]
    zeros = len(decimal) - len(decimal.lstrip("0"))
    t = str(value * int("1" + ("0" * zeros))).split("0.")[1]

    return f"{quote_symbol}0.0({zeros}){t[:2]}"


def price(value: number, quote_symbol: str) -> str:
    return (
        f"{quote_symbol}{value:,.0f}"
        if value >= 10_000
        else f"{quote_symbol}{value:,.0f}"
        if 10_000 > value >= 1_000
        else f"{quote_symbol}{value:,.2f}"
        if 1_000 > value >= 100
        else f"{quote_symbol}{value:,.3f}"
        if 100 > value >= 1
        else f"{quote_symbol}{value:,.4f}"
        if 1 > value >= 0.001
        else price_indented(value, quote_symbol)
    )


def change_percent(value: number) -> str:
    symbol = "▲" if value >= 0.00 else "▼"
    value_symbol = "+" if value >= 0.00 else "-"
    abs_value = abs(value)
    x_count = (abs_value // 100) + (1 if value >= 0.00 else 0)

    return (
        f"{symbol} {value_symbol}{abs_value // 1_000:,.0f}K%"
        if x_count >= 100
        else f"{symbol} {value_symbol}{abs_value:,.0f}%"
        if 100 > x_count > 1
        else f"{symbol} {value_symbol}{abs_value:.2f}%"
    )


def market_cap(value: number, quote_symbol: str) -> str:
    return (
        f"{quote_symbol}{(value / 10**9):,.0f}B"
        if 1_000 > value // 10**12 >= 1
        else f"{quote_symbol}{(value / 10**9):,.2f}B"
        if 1_000 > value // 10**9 >= 1
        else f"{quote_symbol}{(value / 10**6):,.2f}M"
        if 1_000 > value // 10**6 >= 1
        else f"{quote_symbol}{(value / 10**3):,.2f}K"
        if 1_000 > value // 10**3 >= 1
        else f"{quote_symbol}{(value / 10**3):,.2f}K"
    )


def name(n: str) -> str:
    return n if len(n) < 10 else f"{n[:8]}..."


def timestamp(dt: datetime.datetime) -> str:
    return f"{
        dt
        .replace(tzinfo=datetime.timezone.utc)
        .strftime("%Y-%m-%d %H:%M:%S")
    } (UTC +0)"
