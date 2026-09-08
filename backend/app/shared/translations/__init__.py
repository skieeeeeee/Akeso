"""Regional-language translations, one module per language.

Kept out of the content modules on purpose. Marathi, Tamil, Gujarati and
Punjabi were authored after the fact and need review by a speaker of each,
which is only practical if the translations sit in one flat, readable file per
language rather than scattered as a fourth keyword argument across a thousand
`t()` calls.

Each file maps the **English source string** to its translation. English is
the key because that is what a reviewer reads, and because the same English
string always means the same thing in this application.

`t()` consults these overlays for any language it was not given explicitly,
so an inline `mr=` argument always wins over the overlay — that is how a
translation gets corrected in place if the overlay is ever wrong.
"""

from __future__ import annotations

from app.shared.translations.gu import GUJARATI
from app.shared.translations.mr import MARATHI
from app.shared.translations.pa import PUNJABI
from app.shared.translations.ta import TAMIL

# Keyed by language code, as used by `Language`.
OVERLAYS: dict[str, dict[str, str]] = {
    "mr": MARATHI,
    "ta": TAMIL,
    "gu": GUJARATI,
    "pa": PUNJABI,
}

__all__ = ["OVERLAYS"]
