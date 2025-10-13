"""Helpers for combining generated panels into grids."""

from __future__ import annotations

from io import BytesIO
from typing import Iterable

from PIL import Image


def compose_grid(panel_images: Iterable[bytes], *, size: tuple[int, int] = (512, 512)) -> bytes:
    images = [Image.open(BytesIO(content)).resize(size) for content in panel_images]
    if len(images) != 4:
        raise ValueError("Expected four panels for grid composition")
    width, height = size
    canvas = Image.new("RGB", (width * 2, height * 2))
    positions = [(0, 0), (width, 0), (0, height), (width, height)]
    for img, position in zip(images, positions, strict=False):
        canvas.paste(img, position)
    output = BytesIO()
    canvas.save(output, format="PNG")
    return output.getvalue()
