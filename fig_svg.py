"""Standalone styling for the documentation SVGs: every colour and font as an attribute on its own element.

Viewers that sanitise SVG drop <style> blocks, and a <rect> without a fill is then black, hiding its text. So the figure
scripts mark elements with the class names below and `inline_styles` replaces each class by attributes.
"""
import re

_FONT = 'font-family="Helvetica, Arial, sans-serif"'
_RAMPS = {  # class -> fill, stroke, title text, subtitle text
    "c-teal": ("#E1F5EE", "#0F6E56", "#085041", "#0F6E56"),
    "c-pink": ("#FBEAF0", "#993556", "#72243E", "#993556"),
    "c-gray": ("#F1EFE8", "#5F5E5A", "#444441", "#5F5E5A"),
}


def _th(col):
    return f'{_FONT} font-size="14" font-weight="500" fill="{col}"'


def _ts(col):
    return f'{_FONT} font-size="12" fill="{col}"'


def _group(m):
    fill, stroke, title, sub = _RAMPS[m.group(1)]
    inner = m.group(2).replace("<rect ", f'<rect fill="{fill}" stroke="{stroke}" ')
    inner = inner.replace('class="th"', _th(title)).replace('class="ts"', _ts(sub))
    return f"<g>{inner}</g>"


def inline_styles(svg):
    """`svg` with its classes replaced by presentation attributes. Fails if a class is left over."""
    svg = re.sub(r'<g class="(c-\w+)">(.*?)</g>', _group, svg, flags=re.S)
    for cls, attrs in (("th", _th("#2C2C2A")), ("ts", _ts("#5F5E5A")),
                       ("tb", f'{_FONT} font-size="12" font-weight="500" fill="#2C2C2A"'),
                       ("box", 'fill="#F8F7F3" stroke="#B4B2A9"'),
                       ("badge", 'fill="#FFFFFF" stroke="#2C2C2A" stroke-width="0.8"')):
        svg = svg.replace(f'class="{cls}"', attrs)
    assert "class=" not in svg and "<style" not in svg
    return svg
