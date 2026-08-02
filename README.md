# Codex Marketplace Template

Plantilla pública para crear un marketplace de plugins de Codex desde tu propia cuenta de GitHub, con catálogo web en GitHub Pages.

## Crear tu marketplace

1. En GitHub, selecciona **Use this template** → **Create a new repository**.
2. Elige el propietario, nombre y visibilidad de tu nuevo repositorio.
3. Sustituye los valores `YOUR_GITHUB_USER`, `YOUR_MARKETPLACE_NAME` y `YOUR_DISPLAY_NAME`.
4. Edita `.agents/plugins/marketplace.json` y agrega tus plugins bajo `plugins/`.
5. Actualiza `docs/catalog.json` con el nombre, descripción, versión y enlace de cada plugin.
6. En **Settings → Pages**, selecciona **GitHub Actions** como fuente si GitHub no lo habilita automáticamente.
7. Haz push a `main`; el workflow publicará el catálogo en `https://YOUR_GITHUB_USER.github.io/YOUR_REPOSITORY/`.

## Estructura

```text
.
├── .agents/plugins/marketplace.json  # Catálogo instalable de Codex
├── .github/workflows/pages.yml       # Despliegue automático
├── docs/                             # GitHub Page del catálogo
│   ├── catalog.json                  # Datos visibles del catálogo
│   ├── index.html
│   ├── app.js
│   ├── styles.css
│   ├── llms.txt
│   ├── robots.txt
│   └── sitemap.xml
└── plugins/example-plugin/           # Plugin de ejemplo reemplazable
```

## Añadir un plugin

Cada plugin necesita un manifiesto `.codex-plugin/plugin.json` y sus skills dentro de `skills/`. Después agrega una entrada equivalente en `.agents/plugins/marketplace.json` y una ficha en `docs/catalog.json`.

## Autoría y licencia

Reemplaza el autor de ejemplo en los manifiestos, README y datos estructurados. Esta plantilla no impone una licencia: añade la licencia que corresponda antes de distribuir tus plugins.
