# ACO — editable video timelines

Choose editing units from what the user needs to select, trim, move or restyle independently. A footage timeline needs independent authored clip nodes; a decorative wrapper should not become a separate selectable track merely because it is a div. Name layers and compositions for visible content, not implementation counters.

Expose content and useful variation as typed props with defaults and constrained schemas. Validate before preview and export, using the same normalized values. Avoid adding dozens of controls for constants that the user never changes. Dynamic metadata belongs in the supported metadata calculation hook; keep truly static composition metadata simple.

When Studio source editing is requested, inspect the installed version's interactivity support. Use supported interactive components, readable inline per-instance values and supported keyframe expressions where the source parser needs them. Rendering correctness does not imply source-editing compatibility. Do not impose inline-only code on projects that do not request visual source editing.

Test the actual operation: select the intended item, change text/style/timing, verify the source diff, reload and confirm persistence. After extracting a subcomposition, inspect both its standalone view and the parent for frame offsets, inherited styles, asset paths and clip length. If the installed release lacks an editor feature, retain editable source/props and state that limitation instead of inventing a panel.
