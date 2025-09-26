
class Keyboard:
    def __init__(self):
        self.layouts = {
            "QWERTY_LOWER": [
                ["q", "w", "e", "r", "t", "y", "u", "i", "o", "p"],
                ["a", "s", "d", "f", "g", "h", "j", "k", "l", ";"],
                ["z", "x", "c", "v", "b", "n", "m", ",", ".", "/"],
                ["Space", "<-", "Shift", "MODE", "RES"]
            ],
            "QWERTY_UPPER": [
                ["Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P"],
                ["A", "S", "D", "F", "G", "H", "J", "K", "L", ":"],
                ["Z", "X", "C", "V", "B", "N", "M", "<", ">", "?"],
                ["Space", "<-", "Shift", "MODE", "RES"]
            ],
            "NUMPAD": [
                ["7", "8", "9"],
                ["4", "5", "6"],
                ["1", "2", "3"],
                ["0", "<-", "MODE", "RES"]
            ],
            "YES/NO": [
                ["YES", "NO"],
                ["<-", "MODE", "RES"]
            ]
        }
        self.layout_names = list(self.layouts.keys())
        self.current_layout_name = "QWERTY_LOWER"
        self.is_shifted = False

    def get_keys(self):
        return self.layouts[self.current_layout_name]

    def switch_layout(self):
        current_index = self.layout_names.index(self.current_layout_name)
        next_index = (current_index + 1) % len(self.layout_names)
        self.current_layout_name = self.layout_names[next_index]

    def toggle_shift(self):
        self.is_shifted = not self.is_shifted
        if self.is_shifted:
            self.current_layout_name = "QWERTY_UPPER"
        else:
            self.current_layout_name = "QWERTY_LOWER"
