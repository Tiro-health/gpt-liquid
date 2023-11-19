def make_quote(text):
    return "\n".join([f">{line}" for line in text.splitlines()])


def make_key_value_table(data):
    return "| key | value |\n|---|---|\n" + "\n".join(
        [f"| {key} | {value} |" for key, value in data.items()]
    )
