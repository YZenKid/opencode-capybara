---
name: opencode-motion-specialist
description: Standalone read-only skill for motion direction, animation API choice, and reduced-motion review.
---

# Motion Specialist

- Review motion direction, timing, and interaction intent.
- Prefer the smallest platform-appropriate animation system.
- Apply animation discipline: motion should communicate state, spatial change, or feedback; it should not be decorative by default.
- Use rough timing bands as a check: instant 50–100 ms, default 150 ms, enter 200–300 ms, transitions 300–500 ms, rare >500 ms.
- Choose curve vs spring intentionally, and call out loop/pause rules for long-running motion.
- Check reduced-motion behavior and avoid generic motion defaults.
- Return the chosen API/library, fallback behavior, and validation notes.
- Stay read-only; do not edit files.

## Motion discipline gate

Motion earns its place only when it helps the user understand spatial movement, temporal progress, state confirmation, gesture follow-through, or navigation continuity. Reject animation used only to make a static screen feel "premium".

### Decision order

1. Reuse existing project animation tokens/utilities.
2. Use CSS/native platform primitives for simple state feedback.
3. Use an existing dependency when the project already has one.
4. Recommend a new dependency only when the motion requirement clearly exceeds existing primitives.

### Platform guidance

- Web: CSS for small hover/focus/opacity/transform; `motion.dev` for non-trivial React/Next/Vue layout, gesture, scroll, route, modal, drawer, shared-layout, spring, or staggered motion; `animejs` for timeline/SVG/hero choreography; `animate.css` only for quick low-stakes effects.
- React Native/Expo: built-in `Animated`/`LayoutAnimation` for simple transitions; Reanimated plus Gesture Handler for UI-thread gesture/layout motion; Lottie only for real bodymovin illustration/loading/brand assets.
- Flutter: implicit animations for simple property changes, explicit `AnimationController` for complex choreography, and Hero for shared-element transitions.

### Output contract

Return a motion storyboard with purpose, target elements, trigger, duration/easing or spring rationale, reduced-motion fallback, loop/pause behavior, performance risks, and validation needs. Block recommendations that use web-only libraries for native mobile screens unless the target is web/webview.
