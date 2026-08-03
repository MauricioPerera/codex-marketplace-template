# Instrucciones para agentes de IA

Este repositorio es una plantilla para marketplaces públicos de plugins de Claude Code y Codex. Al modificarlo, conservar la estructura y trabajar con cambios pequeños, verificables y reversibles.

## Fuentes de verdad

- `.claude-plugin/marketplace.json`: catálogo instalable por Claude Code. Usa `source` como ruta relativa `./plugins/<plugin-name>`.
- `.agents/plugins/marketplace.json`: catálogo instalable por Codex. La lista `plugins[]` define qué plugins ofrece el marketplace.
- `plugins/<plugin-name>/.claude-plugin/plugin.json`: identidad, versión, autoría y metadata de cada plugin para Claude Code.
- `plugins/<plugin-name>/.codex-plugin/plugin.json`: identidad, versión, autoría y metadata de cada plugin para Codex.
- `plugins/<plugin-name>/skills/`: skills incluidas en el plugin.
- `docs/catalog.json`: datos visibles en la GitHub Page. Debe mantenerse sincronizado con `marketplace.json`.
- `docs/index.html`, `docs/app.js` y `docs/styles.css`: presentación y comportamiento del catálogo.
- `docs/robots.txt`, `docs/sitemap.xml` y `docs/llms.txt`: descubrimiento por buscadores y sistemas de IA.
- `.github/workflows/pages.yml`: despliegue de la GitHub Page. No cambiarlo salvo que se modifique la estrategia de publicación.
- `.github/workflows/marketplace-validation.yml`: gate automático para manifests, rutas, skills y JSON.
- `scripts/validate_marketplace.py`: validador local equivalente al gate de CI; comprueba sincronización del catálogo y coherencia de nombres, versiones y display names entre manifests.
- `scripts/validate_all.py`: ejecuta la suite unificada que usa CI.
- `scripts/configure_marketplace.py`: reemplaza de forma segura los placeholders `YOUR_*` al iniciar un marketplace nuevo.

## Flujo para agregar un plugin

1. Normalizar el nombre en minúsculas con guiones: `mi-plugin`.
2. Crear `plugins/mi-plugin/.claude-plugin/plugin.json` y `plugins/mi-plugin/.codex-plugin/plugin.json` con metadata equivalente.
3. Añadir al menos una skill bajo `plugins/mi-plugin/skills/mi-plugin/SKILL.md`.
4. Añadir la entrada Claude a `.claude-plugin/marketplace.json` con `source: "./plugins/mi-plugin"` y la entrada Codex a `.agents/plugins/marketplace.json` con `source.path` relativo `./plugins/mi-plugin`.
5. Añadir una ficha equivalente a `docs/catalog.json`, incluyendo nombre visible, versión, categoría, descripción, capacidades y URL de GitHub.
6. Actualizar `docs/llms.txt` si cambia la identidad, URL o instrucciones operativas del marketplace.
7. Reemplazar cualquier placeholder `YOUR_*` si el repositorio ya fue personalizado.
8. Ejecutar `python scripts/validate_marketplace.py`, la validación JSON y `node --check docs/app.js` antes de hacer commit.

## Flujo para actualizar un plugin

1. Leer primero el manifiesto, la skill y el registro de `marketplace.json`.
2. Incrementar `version` siguiendo semver cuando cambie el comportamiento o el contenido.
3. Mantener sincronizadas la versión y descripción en `docs/catalog.json`.
4. No borrar una skill, cambiar el nombre del plugin, cambiar el autor o modificar la licencia sin confirmación explícita.
5. No inventar integraciones, capacidades, fuentes o enlaces que no existan en el repositorio.

## Validación

Desde la raíz del repositorio, ejecutar:

```powershell
python scripts/validate_all.py
```

También comprobar por etapas:

```powershell
python <ruta-a-codex>/skills/.system/plugin-creator/scripts/validate_plugin.py plugins/mi-plugin
python <ruta-a-codex>/skills/.system/skill-creator/scripts/quick_validate.py plugins/mi-plugin/skills/mi-plugin
```

El validador comprueba que ambos marketplaces contengan los mismos plugins y categorías, que cada plugin tenga manifests Claude y Codex coherentes, que exista al menos una skill y que `docs/catalog.json` esté sincronizado. También comprobar que ambos `marketplace.json`, ambos `plugin.json` y `docs/catalog.json` sean JSON válidos, que `docs/sitemap.xml` sea XML válido y que los enlaces de `docs/robots.txt` y `docs/llms.txt` usen la URL pública correcta.

## Publicación

- Trabajar en una rama descriptiva cuando el cambio requiera revisión.
- Revisar `git diff` y `git status` antes de hacer commit.
- No subir secretos, tokens, archivos `.env`, credenciales ni artefactos de `__pycache__`.
- Hacer push a `main` solo cuando las validaciones hayan pasado y el usuario haya autorizado publicar.
- El workflow de Pages publica `docs/` automáticamente después del push.
- Si Pages falla por primera configuración, habilitar **Settings → Pages → GitHub Actions** y relanzar el workflow.

## Acciones que requieren confirmación

Pedir confirmación antes de: eliminar plugins o skills, cambiar autoría, añadir una licencia, cambiar la URL pública, hacer el repositorio privado, modificar permisos de GitHub o publicar cambios no validados.
