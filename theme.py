"""Космическая тема JARVIS: цвета, шрифты и стили.

Всё оформление приложения собрано здесь, чтобы вид менялся в одном месте.
"""

from __future__ import annotations

import tkinter as tk
from tkinter import ttk

# --- палитра ---------------------------------------------------------------
BG = "#05070f"          # глубокий космос
PANEL = "#080d1a"       # панели шапки и статуса
CHAT_BG = "#070b14"     # фон чата
INPUT_BG = "#0d1526"    # поле ввода
BORDER = "#16233a"      # тонкие рамки
ACCENT = "#35e0ff"      # неоновый циан (дуга реактора)
ACCENT_DIM = "#0d3a4d"
ACCENT_DARK = "#0b2b3a"
TEXT = "#dbe9ff"
TEXT_DIM = "#9fb6d4"
MUTED = "#5d7ba0"
SELECT = "#1b3a5c"
WARN = "#ffb347"
ERROR = "#ff5c7a"
TOOL = "#4a6a8f"
RESULT = "#3f5a78"
USER = "#8f7bff"

FONT = ("Segoe UI", 10)
FONT_SMALL = ("Segoe UI", 8)
FONT_MONO = ("Consolas", 9)


def blend(color_a: str, color_b: str, t: float) -> str:
    """Смешивает два цвета #rrggbb: t=0 → a, t=1 → b."""
    t = max(0.0, min(1.0, t))
    a = [int(color_a[i : i + 2], 16) for i in (1, 3, 5)]
    b = [int(color_b[i : i + 2], 16) for i in (1, 3, 5)]
    return "#" + "".join(f"{round(x + (y - x) * t):02x}" for x, y in zip(a, b))


def apply(root: tk.Tk) -> None:
    """Тёмная тема для ttk-виджетов (скроллбары и т. п.)."""
    style = ttk.Style(root)
    try:
        style.theme_use("clam")
    except tk.TclError:
        pass
    style.configure(
        "Jarvis.Vertical.TScrollbar",
        background=BORDER,
        troughcolor=CHAT_BG,
        bordercolor=CHAT_BG,
        arrowcolor=MUTED,
        darkcolor=BORDER,
        lightcolor=BORDER,
        relief="flat",
    )
    style.map(
        "Jarvis.Vertical.TScrollbar",
        background=[("active", ACCENT_DARK)],
        arrowcolor=[("active", ACCENT)],
    )


def button(
    parent: tk.Misc,
    text: str,
    command,
    accent: bool = False,
    small: bool = False,
) -> tk.Button:
    """Плоская кнопка в стиле интерфейса Джарвиса."""
    bg = ACCENT_DARK if accent else "#101a2e"
    fg = ACCENT if accent else TEXT_DIM
    return tk.Button(
        parent,
        text=text,
        command=command,
        bd=0,
        relief="flat",
        bg=bg,
        fg=fg,
        activebackground="#1b2b4a",
        activeforeground=ACCENT,
        font=("Segoe UI", 8 if small else 9),
        padx=6 if small else 12,
        pady=1 if small else 5,
        cursor="hand2",
        highlightthickness=0,
    )


def check(parent: tk.Misc, text: str, variable: tk.Variable, command) -> tk.Checkbutton:
    """Тёмный чекбокс без рамки."""
    return tk.Checkbutton(
        parent,
        text=text,
        variable=variable,
        command=command,
        bd=0,
        relief="flat",
        bg=BG,
        fg=TEXT_DIM,
        activebackground=BG,
        activeforeground=ACCENT,
        selectcolor=INPUT_BG,
        font=("Segoe UI", 8),
        highlightthickness=0,
        cursor="hand2",
    )
