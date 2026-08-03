# Claude Code + Codex Marketplace Template

Plantilla pública para crear un marketplace de plugins de Claude Code y Codex desde tu propia cuenta de GitHub, con catálogo web en GitHub Pages.

## Crear tu marketplace

1. En GitHub, selecciona **Use this template** → **Create a new repository**.
2. Elige el propietario, nombre y visibilidad de tu nuevo repositorio.
3. Personaliza la plantilla con el configurador:

   ```bash
   python scripts/configure_marketplace.py --github-user TU_USUARIO --repository TU_REPOSITORIO --marketplace-name tu-marketplace --display-name "Tu Nombre"
   ```

   También puedes añadir `--dry-run` para revisar los archivos que cambiará.
4. Edita `.agents/plugins/marketplace.json` y `.claude-plugin/marketplace.json`, y agrega tus plugins bajo `plugins/`.
5. Actualiza `docs/catalog.json` con el nombre, descripción, versión y enlace de cada plugin.
6. En **Settings → Pages**, selecciona **GitHub Actions** como fuente si GitHub no lo habilita automáticamente.
7. Haz push a `main`; CI validará manifests, skills, JSON y JavaScript antes de publicar el catálogo en `https://YOUR_GITHUB_USER.github.io/YOUR_REPOSITORY/`.

## Uso con agentes de IA

Consulta [AGENTS.md](AGENTS.md) antes de pedir a una IA que agregue o actualice plugins. Allí se documentan las fuentes de verdad, el flujo de sincronización, las validaciones, la publicación y las acciones que requieren confirmación.

Consulta también [SECURITY.md](SECURITY.md) y [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md) antes de abrir issues o pull requests.

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

Cada plugin compatible con ambas plataformas necesita esta estructura:

```text
plugins/mi-plugin/
├── .claude-plugin/plugin.json
├── .codex-plugin/plugin.json
└── skills/mi-plugin/SKILL.md
```

Los dos manifests deben conservar el mismo `name`, `version` y nombre visible. Después agrega una entrada equivalente en ambos marketplaces y una ficha en `docs/catalog.json`.

## Validación y publicación

Antes de hacer commit, ejecuta desde la raíz:

```bash
python scripts/validate_all.py
```

El equivalente por etapas es:

```bash
python scripts/validate_marketplace.py
python -m json.tool .claude-plugin/marketplace.json > /dev/null
python -m json.tool .agents/plugins/marketplace.json > /dev/null
node --check docs/app.js
```

El workflow `Validate marketplace` ejecuta estos controles en cada push y pull request. Comprueba manifests, rutas de plugins, skills, versiones, nombres visibles, categorías y sincronización con `docs/catalog.json`. El workflow `Deploy catalog to GitHub Pages` publica `docs/` cuando la rama `main` recibe cambios.

Los workflows usan `actions/checkout@v6` y optan por Node.js 24. Si utilizas runners autoalojados, mantenlos en una versión compatible con ese runtime.

## Instalación

En Claude Code, desde la terminal:

```text
claude plugin marketplace add YOUR_GITHUB_USER/YOUR_REPOSITORY
claude plugin install example-plugin@YOUR_MARKETPLACE_NAME-claude
```

En Codex, registra el marketplace desde Plugins y busca `example-plugin`. En Claude Desktop usa `+ → Plugins → Add plugin`; los comandos `/plugin` solo funcionan dentro de la interfaz interactiva de Claude Code.

La página también ofrece botones de instalación para copiar los comandos de cada plataforma.

## Autoría y licencia

Reemplaza el autor de ejemplo en los manifiestos, README y datos estructurados. La plantilla se distribuye bajo la [licencia MIT](LICENSE); revisa también las licencias de los plugins y activos que agregues.
