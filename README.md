# Claude Code + Codex Marketplace Template

Plantilla pública para crear un marketplace de plugins de Claude Code y Codex desde tu propia cuenta de GitHub, con catálogo web en GitHub Pages.

## Crear tu marketplace

1. En GitHub, selecciona **Use this template** → **Create a new repository**.
2. Elige el propietario, nombre y visibilidad de tu nuevo repositorio.
3. Sustituye los valores `YOUR_GITHUB_USER`, `YOUR_MARKETPLACE_NAME` y `YOUR_DISPLAY_NAME`.
4. Edita `.agents/plugins/marketplace.json` y `.claude-plugin/marketplace.json`, y agrega tus plugins bajo `plugins/`.
5. Actualiza `docs/catalog.json` con el nombre, descripción, versión y enlace de cada plugin.
6. En **Settings → Pages**, selecciona **GitHub Actions** como fuente si GitHub no lo habilita automáticamente.
7. Haz push a `main`; el workflow publicará el catálogo en `https://YOUR_GITHUB_USER.github.io/YOUR_REPOSITORY/`.

## Uso con agentes de IA

Consulta [AGENTS.md](AGENTS.md) antes de pedir a una IA que agregue o actualice plugins. Allí se documentan las fuentes de verdad, el flujo de sincronización, las validaciones, la publicación y las acciones que requieren confirmación.

## Estructura

```text
.
├── .claude-plugin/marketplace.json   # Catálogo instalable de Claude Code
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

Cada plugin compatible con ambas plataformas necesita `.claude-plugin/plugin.json` y `.codex-plugin/plugin.json`. Sus skills compartidas viven en `skills/`. Después agrega una entrada equivalente en ambos marketplaces y una ficha en `docs/catalog.json`.

## Instalación

En Claude Code, desde la terminal:

```text
claude plugin marketplace add YOUR_GITHUB_USER/YOUR_REPOSITORY
claude plugin install example-plugin@YOUR_MARKETPLACE_NAME-claude
```

En Codex, registra el marketplace desde Plugins y busca `example-plugin`. En Claude Desktop usa `+ → Plugins → Add plugin`; los comandos `/plugin` solo funcionan dentro de la interfaz interactiva de Claude Code.

## Autoría y licencia

Reemplaza el autor de ejemplo en los manifiestos, README y datos estructurados. Esta plantilla no impone una licencia: añade la licencia que corresponda antes de distribuir tus plugins.
