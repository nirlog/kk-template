# KORSAC web assets

Approved masters остаются в родительской директории и не изменяются.
`korsac-mark.svg` ← ICON; `korsac-wordmark.svg` ← TEXT;
`korsac-lockup-stacked.svg` ← V1; `korsac-lockup-horizontal.svg` ← V2.

Static derivatives: external SVG, eyes off, без glow filter/animation.
`korsac-mark-motion.svg` ← ICON: eyes-off template с original localized filter.
Hero/UI Kit inline copies используют собственные `home-brand-` / `kit-brand-`
prefixes. CSS/JS controller находится вне SVG; без enhancement глаза off.

Geometry, palette, metallic gradients и viewBox сохранены. При обновлении
approved master нужно заново подготовить derivatives и синхронизировать
две inline copies, переписав все IDs и fragment references.

[Usage / timing / accessibility / isolation](../../../../docs/frontend/KORSAC-BRAND-ASSET-INTEGRATION.md).
