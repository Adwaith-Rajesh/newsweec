from typing import List


# check button

class CheckBoxButton:

    def __init__(self, text, state=None) -> None:
        self.text = text
        self.state = state or False

    @property
    def button(self) -> List[str]:
        if self.state:
            sym = "✔️"
        else:
            sym = "❌"

        return [sym, self.text]

    @property
    def flip(self) -> None:
        self.state = not self.state


def flip(names: List[str], buttons: List[CheckBoxButton]) -> List[CheckBoxButton]:
    """flips the checkbox button to the opposite of what it is"""
    new_buttons = []
    for button in buttons:
        if button.text in names:
            button.flip

        new_buttons.append(button)
    return new_buttons


def checkbox_generator(labels: List[str]) -> List[CheckBoxButton]:
    return [CheckBoxButton(t) for t in labels]
