def parse_float_list(text: str):
    return [float(value.strip()) for value in text.split(",") if value.strip()]
