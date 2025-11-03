# Cocorels V3 Usage Guide

## Compiling and Running
- Dependencies: Java 8+, `SimpleJson`, `Action`, `Corel`, `CorelEvaluation`, `NativeEpuBindings`.
- Compile: `javac *.java`.
- Run: `java CocorelsV3Skeleton`.

## Example
```java
Map<String, Object> ctx = new HashMap<>();
ctx.put("legal_status", "legal");
Action action = new Action("Distribute resources", ctx);
CocorelsV3Skeleton core = new CocorelsV3Skeleton(SimpleJson.parse("{}"));
Map<String, CorelEvaluation> results = core.evaluate(action, Corel.FAIR.opcode, 123L, 1500, false, 100);
// Expected: FAIR -> [score=0.8, provenance=edge: heuristic]