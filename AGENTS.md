# Instrucciones para agentes de IA

Este repositorio es una plantilla para marketplaces públicos de plugins de Codex. Al modificarlo, conservar la estructura y trabajar con cambios pequeños, verificables y reversibles.

## Fuentes de verdad

- `.agents/plugins/marketplace.json`: catálogo instalable por Codex. La lista `plugins[]` define qué plugins ofrece el marketplace.
- `plugins/<plugin-name>/.codex-plugin/plugin.json`: identidad, versión, autoría y metadata de cada plugin.
- `plugins/<plugin-name>/skills/`: skills incluidas en el plugin.
- `docs/catalog.json`: datos visibles en la GitHub Page. Debe mantenerse sincronizado con `marketplace.json`.
- `docs/index.html`, `docs/app.js` y `docs/styles.css`: presentación y comportamiento del catálogo.
- `docs/robots.txt`, `docs/sitemap.xml` y `docs/llms.txt`: descubrimiento por buscadores y sistemas de IA.
- `.github/workflows/pages.yml`: despliegue de la GitHub Page. No cambiarlo salvo que se modifique la estrategia de publicación.

## Flujo para agregar un plugin

1. Normalizar el nombre en minúsculas con guiones: `mi-plugin`.
2. Crear `plugins/mi-plugin/.codex-plugin/plugin.json` con `name`, `version`, `description`, `author`, `skills` e `interface` válidos.
3. Añadir al menos una skill bajo `plugins/mi-plugin/skills/mi-plugin/SKILL.md`.
4. Añadir la misma entrada a `.agents/plugins/marketplace.json` con `source.path` relativo `./plugins/mi-plugin`, política y categoría.
5. Añadir una ficha equivalente a `docs/catalog.json`, incluyendo nombre visible, versión, categoría, descripción, capacidades y URL de GitHub.
6. Actualizar `docs/llms.txt` con el plugin y su fuente.
7. Reemplazar cualquier placeholder `YOUR_*` si el repositorio ya fue personalizado.
8. Ejecutar las validaciones antes de hacer commit.

## Flujo para actualizar un plugin

1. Leer primero el manifiesto, la skill y el registro de `marketplace.json`.
2. Incrementar `version` siguiendo semver cuando cambie el comportamiento o el contenido.
3. Mantener sincronizadas la versión y descripción en `docs/catalog.json`.
4. No borrar una skill, cambiar el nombre del plugin, cambiar el autor o modificar la licencia sin confirmación explícita.
5. No inventar integraciones, capacidades, fuentes o enlaces que no existan en el repositorio.

## Validación

Desde la raíz del repositorio, ejecutar:

```powershell
python <ruta-a-codex>/skills/.system/plugin-creator/scripts/validate_plugin.py plugins/mi-plugin
python <ruta-a-codex>/skills/.system/skill-creator/scripts/quick_validate.py plugins/mi-plugin/skills/mi-plugin
```

También comprobar que `marketplace.json` y `docs/catalog.json` son JSON válidos, que `docs/sitemap.xml` es XML válido y que los enlaces de `docs/robots.txt` y `docs/llms.txt` usan la URL pública correcta.

## Publicación

- Trabajar en una rama descriptiva cuando el cambio requiera revisión.
- Revisar `git diff` y `git status` antes de hacer commit.
- No subir secretos, tokens, archivos `.env`, credenciales ni artefactos de `__pycache__`.
- Hacer push a `main` solo cuando las validaciones hayan pasado y el usuario haya autorizado publicar.
- El workflow de Pages publica `docs/` automáticamente después del push.
- Si Pages falla por primera configuración, habilitar **Settings → Pages → GitHub Actions** y relanzar el workflow.

## Acciones que requieren confirmación

Pedir confirmación antes de: eliminar plugins o skills, cambiar autoría, añadir una licencia, cambiar la URL pública, hacer el repositorio privado, modificar permisos de GitHub o publicar cambios no validados.
