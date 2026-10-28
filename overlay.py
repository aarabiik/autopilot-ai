"""Мини-режим JARVIS: маленькое окно поверх экрана, как ассистент в телефоне.

Окно без рамки, всегда сверху, перетаскивается за «реактор». Enter — отправить,
кнопка ⤢ — развернуть в полный режим, Esc — свернуть обратно в мини.
"""

from __future__ import annotations

import math
import tkinter as tk
from typing import Callable

import theme

WIDTH = 400
HEIGHT = 62
ORB = 46


class MiniOverlay(tk.Toplevel):
    """Плавающая мини-панель с полем ввода и пульсирующим реактором."""

    def __init__(
        self,
        master: tk.Misc,
        on_send: Callable[[str], None],
        on_expand: Callable[[], None],
        on_close: Callable[[], None],
    ) -> None:
        super().__init__(master)
        self.on_send = on_send
        self.on_expand = on_expand
        self.on_close = on_close
        self._phase = 0.0
        self._busy = False
        self._drag = (0, 0)
        self._job: str | None = None

        self.overrideredirect(True)
        self.attributes("-topmost", True)
        try:
            self.attributes("-alpha", 0.97)
        except tk.TclError:
            pass
        self.configure(bg=theme.BORDER)

        shell = tk.Frame(self, bg=theme.PANEL, padx=1, pady=1)
        shell.pack(fill="both", expand=True)

        self.canvas = tk.Canvas(
            shell, width=ORB, height=ORB, bg=theme.PANEL, highlightthickness=0
        )
        self.canvas.pack(side="left", padx=(8, 4), pady=8)
        self.canvas.bind("<Button-1>", self._start_drag)
        self.canvas.bind("<B1-Motion>", self._do_drag)

        self.entry = tk.Entry(
            shell,
            bd=0,
            relief="flat",
            bg=theme.INPUT_BG,
            fg=theme.TEXT,
            insertbackground=theme.ACCENT,
            font=("Segoe UI", 10),
            highlightthickness=0,
        )
        self.entry.pack(side="left", fill="both", expand=True, pady=14, padx=(2, 6))
        self.entry.bind("<Return>", lambda _e: self._submit())
        self.entry.bind("<Escape>", lambda _e: self.on_close())
        self.entry.bind("<FocusIn>", lambda _e: self.entry.configure(bg=theme.ACCENT_DARK))
        self.entry.bind("<FocusOut>", lambda _e: self.entry.configure(bg=theme.INPUT_BG))

        self.expand_btn = theme.button(shell, "⤢", self.on_expand, small=True)
        self.expand_btn.pack(side="right", padx=(0, 4))
        self.close_btn = theme.button(shell, "✕", self.on_close, small=True)
        self.close_btn.pack(side="right", padx=(0, 4))

        self._place_default()
        self._animate()

    # -- геометрия ---------------------------------------------------------
    def _place_default(self) -> None:
        self.update_idletasks()
        screen_w = self.winfo_screenwidth()
        screen_h = self.winfo_screenheight()
        x = screen_w - WIDTH - 28
        y = screen_h - HEIGHT - 72
        self.geometry(f"{WIDTH}x{HEIGHT}+{x}+{y}")

    def _start_drag(self, event: tk.Event) -> None:
        self._drag = (event.x_root - self.winfo_x(), event.y_root - self.winfo_y())

    def _do_drag(self, event: tk.Event) -> None:
        dx, dy = self._drag
        self.geometry(f"+{event.x_root - dx}+{event.y_root - dy}")

    # -- реактор -----------------------------------------------------------
    def _animate(self) -> None:
        self._phase = (self._phase + 0.16) % (2 * math.pi)
        self.canvas.delete("all")
        cx = cy = ORB / 2
        pulse = 0.5 + 0.5 * math.sin(self._phase)
        speed = 2.4 if self._busy else 1.0
        radius = 13 + 2.2 * pulse * speed

        for ring, width in ((radius + 8, 1), (radius + 4, 1)):
            color = theme.blend(theme.ACCENT_DARK, theme.ACCENT, 0.25 + 0.35 * pulse)
            self.canvas.create_oval(
                cx - ring, cy - ring, cx + ring, cy + ring, outline=color, width=width
            )
        glow = theme.blend(theme.ACCENT_DARK, theme.ACCENT, 0.35 + 0.5 * pulse)
        self.canvas.create_oval(
            cx - radius, cy - radius, cx + radius, cy + radius,
            outline=glow, width=2,
        )
        core = theme.blend(theme.ACCENT, "#ffffff", 0.25 + 0.45 * pulse)
        self.canvas.create_oval(
            cx - 5, cy - 5, cx + 5, cy + 5, fill=core, outline=""
        )
        self._job = self.after(45, self._animate)

    # -- состояние ---------------------------------------------------------
    def set_busy(self, busy: bool) -> None:
        self._busy = busy
        self.entry.configure(state="disabled" if busy else "normal")
        if not busy:
            self.entry.focus_set()

    def focus_input(self) -> None:
        self.deiconify()
        self.lift()
        self.entry.focus_force()

    def _submit(self) -> None:
        text = self.entry.get().strip()
        if not text or self._busy:
            return
        self.entry.delete(0, "end")
        self.on_send(text)

    def destroy(self) -> None:
        if self._job is not None:
            try:
                self.after_cancel(self._job)
            except Exception:  # noqa: BLE001
                pass
            self._job = None
        super().destroy()
