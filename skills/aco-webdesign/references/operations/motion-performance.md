# Diagnose animation performance

Reproduce dropped frames under a recorded workload. Use a profiler to distinguish main-thread work, layout, paint, compositing and asset cost. Reduce the measured bottleneck and repeat the trace.

For Vite projects, use the [live runtime collector](../framework-tools.md): set the actual refresh rate, capture the same interaction before and after, and export both measurements. Use browser profiling for attribution to scripting, layout, paint or compositing; callback intervals alone do not identify the cause.

Completion evidence: Comparable traces or an explicit statement that runtime profiling was unavailable.

Use the project’s existing conventions and available tools. Report missing capabilities explicitly; a written procedure is not runtime proof.
