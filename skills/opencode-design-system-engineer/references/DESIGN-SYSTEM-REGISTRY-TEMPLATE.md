# Design System Registry Template

Use this template to catalog reusable design-system components, tokens, and primitives. This registry enables @frontend and @mobile to discover and reuse existing work before implementing from scratch.

## Structure

```markdown
# [Project Name] Design System Registry

## Tokens

### Color Tokens
| Token Name | Value | Usage | File Location |
|------------|-------|-------|---------------|
| `primary-500` | `#2563eb` | Primary actions, links | `src/tokens/colors.ts` |
| `neutral-100` | `#f8fafc` | Background surfaces | `src/tokens/colors.ts` |

### Typography Tokens
| Token Name | Value | Usage | File Location |
|------------|-------|-------|---------------|
| `text-body-lg` | `16px/1.5` | Body text, paragraphs | `src/tokens/typography.ts` |
| `heading-xl` | `32px/1.2` | Page headings | `src/tokens/typography.ts` |

### Spacing Tokens
| Token Name | Value | Usage | File Location |
|------------|-------|-------|---------------|
| `space-4` | `16px` | Component padding | `src/tokens/spacing.ts` |
| `space-6` | `24px` | Section spacing | `src/tokens/spacing.ts` |

## Primitives

### Button
| Variant | Props | States | File Location |
|---------|-------|--------|---------------|
| `Primary` | `onClick, children, disabled` | default, hover, focus, active, disabled | `src/components/ui/Button.tsx` |
| `Secondary` | `onClick, children` | default, hover, focus | `src/components/ui/Button.tsx` |
| `Ghost` | `onClick, children` | default, hover | `src/components/ui/Button.tsx` |

### Input
| Variant | Props | States | File Location |
|---------|-------|--------|---------------|
| `Text` | `value, onChange, placeholder` | default, focus, error, disabled | `src/components/ui/Input.tsx` |
| `Textarea` | `value, onChange, rows` | default, focus, error | `src/components/ui/Input.tsx` |

### Card
| Variant | Props | States | File Location |
|---------|-------|--------|---------------|
| `Default` | `children` | default, interactive | `src/components/ui/Card.tsx` |
| `Featured` | `title, children, image` | default | `src/components/ui/Card.tsx` |

## Components (Composed)

### Navigation
| Component | Uses | File Location |
|-----------|------|---------------|
| `TopBar` | `Logo, Menu, Button` | `src/components/Navigation.tsx` |
| `Sidebar` | `Menu, MenuItem, Badge` | `src/components/Sidebar.tsx` |

### Feedback
| Component | Uses | File Location |
|-----------|------|---------------|
| `Toast` | `Icon, Button` | `src/components/Feedback.tsx` |
| `Modal` | `Card, Button, Input` | `src/components/Modal.tsx` |

## Patterns

### Form Pattern
- **File**: `src/patterns/Form.tsx`
- **Uses**: `Input`, `Button`, `Label`, `Error`
- **Variants**: horizontal, vertical, inline
- **Example**: See `src/pages/Login.tsx`

### Card Grid Pattern
- **File**: `src/patterns/CardGrid.tsx`
- **Uses**: `Card`, `Container`
- **Variants**: 2-col, 3-col, 4-col, responsive
- **Example**: See `src/pages/Dashboard.tsx`

## Usage Guidelines

### When to Use Registry
- ✅ Always check registry before implementing new components
- ✅ Reuse existing tokens/primitives/components
- ✅ Extend existing variants before creating new components
- ❌ Do not duplicate existing work
- ❌ Do not create parallel design systems

### How to Contribute
1. Check if component/token already exists in registry
2. If yes, extend or reuse
3. If no, implement following DESIGN.md grammar
4. Update this registry with new entry
5. Notify @frontend/@mobile lanes of new availability

### Discovery for @frontend/@mobile
Before implementing a screen:
1. Read this registry to find existing tokens/primitives/components
2. Use registry entries in implementation
3. If missing, route to @design-system-engineer for registry expansion
4. Do not implement parallel primitives

## Example: Minimal Registry

```markdown
# Dashboard Design System

## Tokens
- `primary-blue`: `#2563eb` → `src/tokens.ts`
- `text-lg`: `16px` → `src/tokens.ts`
- `space-4`: `16px` → `src/tokens.ts`

## Primitives
- `Button` (primary, secondary, ghost) → `src/components/Button.tsx`
- `Card` (default) → `src/components/Card.tsx`
- `Input` (text) → `src/components/Input.tsx`

## Patterns
- `Form` (vertical layout) → `src/patterns/Form.tsx`
```

## Integration with Lanes

- **@designer**: References registry in blueprint handoff
- **@design-system-engineer**: Maintains and expands registry
- **@frontend/@mobile**: Checks registry before implementation, uses existing entries
- **@quality-gate**: Validates output uses registry where applicable
