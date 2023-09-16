color_dict = {
    "red": (219, 40, 40),
    "blue": (29, 128, 243)
}


def get_color(str_color: str):
    return color_dict[str_color.lower()]
