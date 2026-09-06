import Lake
open Lake DSL

-- KSO mechanised core (ORION-V2 theory batch 12, FDX-16).
-- No external dependencies: builds with the pinned toolchain alone (no Mathlib).
package «kso_core» where
  version := v!"0.1.0"

@[default_target]
lean_lib «KsoCore» where
  roots := #[`KsoCore]
