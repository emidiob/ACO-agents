# Framework source editing and components

These original ACO tools integrate into an existing local project. They do not install another agent skill or replace the project's framework. Export from the installed `aco-webdesign` directory to a new directory in that project.

## Vite source editor

```bash
python3 scripts/framework_live.py /project/tools/aco-live
```

Add the exported bridge to the project's existing Vite configuration, preserving its framework plugin and other settings:

```js
import acoLive from './tools/aco-live/aco-vite.mjs';
// Inside the existing defineConfig object:
// plugins: [acoLive(), ...existingPlugins]
// server: { ...existingServerSettings, host: '127.0.0.1' }
```

Use the project's normal development command. Open `/__aco/live` on its local origin (or `<base>/__aco/live` when Vite uses a base path). The bridge uses the documented [Vite plugin hooks](https://vite.dev/guide/api-plugin.html), runs only during development and is absent from production builds.

Place a stable, globally unique literal identifier on each editable native element:

```jsx
<h1 data-aco-edit="home-title" className="hero-title">A specific title</h1>
```

```vue
<h1 data-aco-edit="home-title" class="hero-title">A specific title</h1>
```

Select the element in the preview. The editor resolves its file and hash, then saves static text or literal class/className values. Vite performs its normal HMR; component state retention follows the framework's normal refresh boundaries. Switch to interaction mode to use the application. Repeated rendered instances of one source element share its edit. Duplicate identifiers in distinct source locations are refused.

The independent lexical mapper is deliberately conservative. Supported files are UTF-8 `.jsx`, `.tsx`, `.vue` templates and `.html`. It rejects strings/comments, nested or expression-based text, dynamic classes and ambiguous bindings. JSX inside expression-generated fragments may be unavailable. Edit these cases in the source editor; this bridge is not a complete JavaScript/TypeScript parser or automatic component source-map engine. Class changes must refer to actual project styles; the tool does not invent utility classes or modify CSS files.

Undo/redo holds 50 edits in the current server session. Stale hashes and external modifications block overwrites. Writes use same-directory atomic replacement. The bridge accepts loopback clients only and requires a session token plus matching origin for mutations. Keep project code trusted. Symlinks, hidden paths, vendor directories and files larger than 2 MB are excluded. Existing Vite CSP, iframe restrictions or unusual proxies can prevent the preview; preserve those protections and use the normal project preview when needed.

## Framework-owned components

```bash
python3 scripts/framework_components.py /project/src/aco-react --framework react
python3 scripts/framework_components.py /project/src/aco-vue --framework vue
```

Each export contains eight independently written components and optional `aco.css`: `Button`, `Toggle`, `Checkbox`, `TextField`, `Select`, `Tabs`, `Accordion`, `Dialog`. React targets React 19; Vue targets Vue 3.5. The project supplies its existing framework dependency. Exporting does not install packages. Reuse project styles instead of importing the optional stylesheet when a design system already exists.

| Component | React state API | Vue state API |
|---|---|---|
| Toggle | `pressed`, `defaultPressed`, `onPressedChange` | `v-model:pressed`, `defaultPressed` |
| Checkbox | `checked`, `defaultChecked`, `onCheckedChange`, `label` | `v-model:checked`, `defaultChecked`, `label` |
| TextField | Native input props, `label`, `description`, `error` | `v-model`, `defaultValue`, `label`, `description`, `error` |
| Select | `value`, `defaultValue`, `onValueChange`, `options`, `label` | `v-model`, `defaultValue`, `options`, `label` |
| Tabs / Accordion | `value`, `defaultValue`, `onValueChange`, `items` | `v-model`, `defaultValue`, `items` |
| Dialog | `open`, `onOpenChange`, `title`, children | `v-model:open`, `title`, default slot |

Select options contain `value`, `label` and optional `disabled`. Tabs/accordion items contain `value`, `label`, `content`; tabs also accept `disabled`. In Vue, named slots matching item values can replace text content. Values must be unique strings. Tabs support arrow keys and Home/End while skipping disabled tabs. Accordion expands one item at a time. Dialog uses the browser modal dialog with Escape, focus containment and restoration; the parent owns its open state. Multiple component instances generate independent ARIA IDs.

```jsx
import {Tabs, Dialog} from './aco-react/aco-components.jsx';
<Tabs items={[
  {value: 'overview', label: 'Overview', content: <p>Project overview</p>},
  {value: 'details', label: 'Details', content: <p>Project details</p>}
]} />
<Dialog open={open} onOpenChange={setOpen} title="Project details">
  <p>Application content</p>
</Dialog>
```

These framework components are a separate, explicitly scoped API. The remaining HTML catalog entries are still HTML recipes and are not automatically converted into framework components. Verify controlled/uncontrolled usage, keyboard behavior and application-specific data flows after integration.
