<div align="center">
  
# CTkSpinbox (Pro)
[![PyPI version](https://img.shields.io/pypi/v/ctk-spinbox-pro)](https://pypi.org/project/ctk-spinbox-pro/)
[![Python versions](https://img.shields.io/pypi/pyversions/ctk-spinbox-pro)](https://pypi.org/project/ctk-spinbox-pro/)
[![License](https://img.shields.io/pypi/l/ctk-spinbox-pro)](https://github.com/E1480/ctk-spinbox-pro/blob/master/LICENSE)
[![Downloads](https://img.shields.io/pypi/dm/ctk-spinbox-pro)](https://pypi.org/project/ctk-spinbox-pro/)

A slightly better version of the current [CTkSpinbox](https://github.com/Sheikh-Rashdan/CTkSpinbox?tab=readme-ov-file) Add-on.
Still have some sharp edges(literally) but it's a start.

## How it will look like

<img src="https://raw.githubusercontent.com/E1480/ctk-spinbox-pro/refs/heads/master/images/Recording%202026-07-31%20024719.gif" />

</div>

> [!WARNING]
> This project is still in development so expect some bugs or some inconveniences.

## Installation

pip:
```bash
pip install ctk-spinbox-pro
```
uv:
```bash
uv add ctk-spinbox-pro
```

## Usage

```python
from ctk_spinbox_pro import CTkSpinbox
```

Then use it like any other CustomTkinter widget — it's a `CTkFrame` under the hood, so it supports the usual `.grid()`, `.pack()`, or `.place()` layout methods.

## Parameters

| Parameter | Type | Description | Default |
|:---:|:---:|---|---|
| `width` | `int` | Total widget width (entry + buttons) | `100` |
| `height` | `int` | Total widget height | `50` |
| `button_width` | `int` | Width reserved for the increment/decrement buttons | `100` |
| `button_height` | `int` | Height reserved for the increment/decrement buttons | `50` |
| `step` | `int` | Amount to change per increment/decrement | `1` |
| `value` | `int` | Starting value | `0` |
| `min` | `int` | Minimum allowed value. Set below `0` to allow negative numbers | `0` |
| `max` | `int \| None` | Maximum allowed value. `None` means unbounded |  `None` |
| `on_change` | `Callable[[], Any] \| None` | Called whenever the value changes (typing, scrolling, or +/- buttons) |  `None` |
> [!NOTE]
> Adding floating point numbers in the future.


Any other keyword arguments are passed straight through to the underlying `CTkFrame`.

## Example

```python
import customtkinter as ctk
from ctk_spinbox_pro import CTkSpinbox

app = ctk.CTk()
app.geometry("300x150")

def on_value_change():
    print("Current value:", spinbox.get())

spinbox = CTkSpinbox(
    app,
    value=10,
    min=-50,      # allows negative numbers
    max=100,
    step=5,
    on_change=on_value_change
)
spinbox.pack(pady=20)

app.mainloop()
```

This creates a spinbox starting at `10`, adjustable in steps of `5`, clamped between `-50` and `100` — typing a value out of range, scrolling with the mouse wheel over the widget, or clicking the ▲/▼ buttons will all keep the value within those bounds.

### Reading the value elsewhere

```python
current = spinbox.get()  # returns an int
```

## Features

- Click-and-scroll support: hover over the entry or either button and scroll to increment/decrement
- Keyboard input is validated live — non-numeric characters are blocked as you type
- Optional negative number support (set `min` below `0`)
- Leading-zero input (e.g. `01`) is blocked automatically
- Clamps to `min`/`max` both while typing and via the buttons
- Resets to `0` if left empty on focus loss
