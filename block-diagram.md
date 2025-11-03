+----------------------------+
|      evaluate() called     |
| Params: action, opcode,    |
| dilemmaHash, complexity,   |
| efForce, timeBudget        |
+-------------+--------------+
              |
              v
+----------------------------+
|        EfPreRouter         |
| (Routing Decision Logic)   |
| - Inputs: opcode, hash,    |
|   complexityScore, efForce,|
|   timeBudget               |
| - Decides Prong 1 (Fast)   |
|   or Prong 2 (Wisdom)      |
+-------------+--------------+
              |
     +--------+--------+
     |                 |
     v                 v
+------------+    +---------------------+
| Prong 1:   |    | Prong 2:             |
| Fast Heur- |    | Wisdom Path          |
| istics    |    | - Trait Sub-assessments|
| - Simple  |    | - Conflict Detection  |
|   heuristics|   | - Conflict Resolution |
| - Quick,  |    | - Duty & Core Boosts  |
|   low-latency| | - Aggregation to Corels|
+------------+    +---------------------+
     |                 |
     +--------+--------+
              |
              v
+----------------------------+
|    CorelEvaluation Report  |
| - Score per Corel Virtue   |
| - Justification string     |
+----------------------------+
              |
              v
+----------------------------+
|   Audit & Logging Hooks    |
| (e.g. signAudit stub call) |
+----------------------------+

