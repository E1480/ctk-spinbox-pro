
from typing import Any # noqa
from string import digits
from tkinter import StringVar
from collections.abc import Callable
from customtkinter import CTkFrame, CTkEntry, CTkButton

class CTkSpinbox(CTkFrame):
    def __init__(self,
        *args,
        width: int = 100,
        height: int = 50,
        button_width: int = 100,
        button_height: int = 50,
        step: int = 1,
        value: int = 0,
        max: int | None = None,
        min: int = 0,
        on_change: Callable[[], Any] | None = None,
        **kwargs
    ):
        super().__init__(*args, width=width, height=height, **kwargs)
        self.start_value: int = value
        self._string_value: StringVar = StringVar()
        self.step: int = step
        self.min: int = min
        self.max: int | None = max
        self._on_change: Callable[[], Any] | None = on_change

        self.entry = CTkEntry(
            self,
            width=int(width / 2),
            height=(height - 6),
            border_width=0,
            textvariable=self._string_value
        )
        self.entry.bind("<Key>", self.validate)
        self.entry.bind("<MouseWheel>", self.scroll)
        self._string_value.trace_add("write", self._onchange_validate)
        self.entry.configure(corner_radius=0)
        self.entry.grid(column=0, row=0, rowspan=2)
        self.entry.insert(0, str(self.start_value))

        self.increment = CTkButton(
            self, text="▲",
            width=int(button_width / 2),
            height=int((button_height - 6) / 2),
            command=self.inc_callback
        )
        self.increment.configure(cursor="arrow", corner_radius=0)
        self.increment.bind("<MouseWheel>", self.scroll)
        self.increment.grid(column=1, row=0)

        self.decrement = CTkButton(
            self, text="▼",
            width=int(button_width / 2),
            height=int((button_height - 6) / 2),
            command=self.dec_callback
        )
        self.decrement.configure(cursor="arrow", corner_radius=0)
        self.decrement.bind("<MouseWheel>", self.scroll)
        self.decrement.grid(column=1, row=1)

        self.entry.bind("<FocusOut>", self._remove_focus)

    def inc_callback(self):
        if self.max is not None and self.start_value >= self.max:
            self.start_value = self.max
            return "break"
        self.start_value += self.step
        self._update_entry()

    def dec_callback(self):
        if self.min is not None and self.start_value <= self.min:
            self.start_value = self.min
            return "break"
        self.start_value -= self.step
        self._update_entry()

    def scroll(self, event):
        if event.delta > 0:
            self.inc_callback()
        elif event.delta < 0:
            self.dec_callback()

    def get(self) -> int:
        return self.start_value

    def _update_entry(self):
        self.entry.delete(0, "end")
        self.entry.insert(0, f"{self.start_value}")
        self.entry.update()
        if self._on_change is not None:
            self._on_change()

    def validate(self, event):
        current = self.entry.get()

        # Backspace/delete
        if event.keycode == 8:
            return

        # Leading "-" is only ever valid if negatives are allowed,
        # the field is currently empty, and there isn't one already.
        if event.char == "-":
            if self.min < 0 and current == "" and "-" not in current:
                return
            return "break"

        # Block a leading zero followed by more digits, e.g. "0" -> "01"
        # (but allow "0" itself, and allow "-0" -> "-01" to be blocked too)
        stripped = current.lstrip("-")
        if event.char in digits and stripped == "0":
            return "break"

        if event.char not in digits:
            return "break"

        if self._on_change is not None:
            self._on_change()

    def _remove_focus(self, event):
        if self.entry.get() in ("", "-"):
            self.start_value = 0
            self._string_value.set("0")
            self._update_entry()

    def _onchange_validate(self, *args):
        value = self._string_value.get()

        # Intermediate states while typing — not real numbers yet, don't crash
        if value in ("", "-"):
            return

        self.start_value = int(value)

        if self.start_value <= self.min:
            self.start_value = self.min
            self._string_value.set(str(self.min))
        if self.max is not None and self.start_value >= self.max:
            self.start_value = self.max
            self._string_value.set(str(self.max))
