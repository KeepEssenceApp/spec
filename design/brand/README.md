# Brand resources

A copy of the parts of the brand that the public clients need, so that no public repository depends on a private one.

- `svg/mark-white.svg`, `svg/mark-black.svg`: the mark, for dark and light backgrounds.
- `svg/mark-small-white.svg`, `svg/mark-small-black.svg`: the same mark with one wave, for use when it is shown less than 28 px high.
- `tabbar/today.svg`, `digest.svg`, `notes.svg`, `assistants.svg`: the four tab icons, 24×24, stroke 1.8, following `currentColor`.

Where they come from: the brand resources are kept and generated in the maintainers' `marketing` repository (`brand/`), which is private. That is the only place they are edited; the files here are copies. App icons and favicons are copied from there straight into each client.

How to use them:

- Do not recolour, stretch, outline or redraw these files. Use the white mark on dark backgrounds and the black one on light backgrounds.
- The name is set as text beside the mark, never baked into an image: system font, weight 700, letter-spacing 0.04em. English `Keep Essence`, Chinese `精华`.
- Gold is one value, `#C5A229`, and the mark has one gold dot.
- A selected tab: icon and label in the main text colour, a bolder label, and a short gold line (18×3, rounded) above the icon. The rule on gold is in `../tokens.css`.
