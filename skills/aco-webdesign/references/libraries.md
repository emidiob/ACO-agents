# Components and project libraries

For independently written ACO component recipes and effects, use [interactive tools](interactive-tools.md). Search the catalog, export the relevant sources, integrate them into the project and test their actual behavior.

Keep the project's stack unless changing it solves a real requirement. Verify current APIs, compatibility and terms from official sources before installing or copying components. The examples in this skill require no npm package, network font or image service.

- [shadcn/ui](https://github.com/shadcn-ui/ui): useful configurable component source for appropriate projects; integrate behavior and theme deliberately. Its presence does not guarantee accessibility of a composed page.
- [Radix primitives](https://github.com/radix-ui/primitives): an optional behavior foundation for complex widgets; style it to the project's identity.
- [React Bits](https://github.com/DavidHDev/react-bits): optional visual effects to evaluate in a concrete project. The reviewed license has a Commons Clause restricting component/tool redistribution; ACO does not bundle or port that library.
- [Motion](https://motion.dev/) and [GSAP](https://gsap.com/): optional motion engines; check installed APIs and current terms, load only needed features and respect reduced motion.
- [axe-core](https://github.com/dequelabs/axe-core) and [Lighthouse](https://github.com/GoogleChrome/lighthouse): supporting audit tools, not aesthetic or accessibility certification.

The skill can implement new components with these resources when appropriate; it is not limited to its examples. It does not reproduce upstream databases, browser extensions, hosted design services or full component catalogs. Native ACO means original orchestration, methods and helpers with explicit dependency boundaries.
