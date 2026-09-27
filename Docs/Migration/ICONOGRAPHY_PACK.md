# Iconography migration pack

The canonical asset bundle is built from the current `main` branch of
`sokcrow/Luminos-Character-Maker`.

The build intentionally copies source iconography without resizing or recompression and
produces:

- `Luminous_Iconography_Main.zip`
- `Catalog/icon_manifest.json`
- `Catalog/icon_manifest.csv`
- registry/catalog JavaScript source used by the current application
- Unreal import notes

Current source inventory observed before automation:

- 636 item icon images under `Assets/Icons`
- 14 button/UI images under `Assets/Images/Buttons`
- 1 weather icon sheet under `Assets/Images/Weather`
- 582 local paths referenced by `js/item-icon-registry.js`

The workflow recalculates these numbers from the source repository each run.
