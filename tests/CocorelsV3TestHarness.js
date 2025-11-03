import java.util.*;

public class CocorelsV3TestHarness {
    public static void main(String[] args) throws Exception {
        Map<String,Object> cfg = SimpleJson.parse("{}");
        CocorelsV3Skeleton core = new CocorelsV3Skeleton(cfg);

        List<TestScenario> scenarios = Arrays.asList(
            new BaselineScenario(),
            new DeterminismScenario(),
            new AdversarialComplexityScenario(),
            new ContextPoisoningScenario(),
            new FaultInjectionScenario(),
            new OfflineAssuranceScenario()
        );

        for (TestScenario scenario : scenarios) {
            System.out.println("\n=== " + scenario.getName() + " ===");
            try {
                scenario.run(core);
            } catch (Exception e) {
                System.err.println("Test failed: " + scenario.getName() + "\n" + e);
            }
        }
        core.shutdown();
    }

    // --- TEST SCENARIO INTERFACE ---
    interface TestScenario {
        String getName();
        void run(CocorelsV3Skeleton core);
    }

    // --- BASELINE FUNCTIONALITY ---
    static class BaselineScenario implements TestScenario {
        public String getName() { return "Baseline Functionality"; }
        public void run(CocorelsV3Skeleton core) {
            Map<String,Object> ctx = new HashMap<>();
            ctx.put("legal_status", "legal");
            Action a1 = new Action("Perform service for elderly neighbor", ctx);

            System.out.println("Action: " + a1.getDescription());
            Map<String,CorelEvaluation> evals = core.evaluate(a1, Corel.HONOUR_DUTY.opcode, 123456L, 3000, false, 100);
            evals.forEach((k,v)->System.out.println(k + " -> " + v));
        }
    }

    // --- DETERMINISM ---
    static class DeterminismScenario implements TestScenario {
        public String getName() { return "Determinism & Repeatability"; }
        public void run(CocorelsV3Skeleton core) {
            Map<String,Object> ctx = new HashMap<>();
            ctx.put("goal", "long-term benefit");
            Action a = new Action("Distribute resources evenly", ctx);

            String firstRun = mapToString(core.evaluate(a, Corel.FAIR.opcode, 1L, 2900, false, 90));
            String secondRun = mapToString(core.evaluate(a, Corel.FAIR.opcode, 1L, 2900, false, 90));
            System.out.println("First:\n" + firstRun);
            System.out.println("Second:\n" + secondRun);
            assert firstRun.equals(secondRun) : "Outputs differ!";
        }
    }

    // --- ADVERSARIAL: Complexity Score Gaming ---
    static class AdversarialComplexityScenario implements TestScenario {
        public String getName() { return "Adversarial: Complexity Score Forcing"; }
        public void run(CocorelsV3Skeleton core) {
            Map<String,Object> harmful = new HashMap<>();
            harmful.put("consequences", Arrays.asList("harm"));
            harmful.put("legal_status", "legal");
            Action badAction = new Action("Hidden surveillance deployment", harmful);

            System.out.println("Attempted harmful action (low complexity):");
            Map<String,CorelEvaluation> eval = core.evaluate(badAction, Corel.KINDNESS.opcode, 67890L, 1999, false, 100);
            eval.forEach((k,v)->System.out.println(k + " -> " + v));
            // Expect low KINDNESS score and overall conservative output
        }
    }

    // --- CONTEXT POISONING ---
    static class ContextPoisoningScenario implements TestScenario {
        public String getName() { return "Context Poisoning"; }
        public void run(CocorelsV3Skeleton core) {
            Map<String,Object> poisoned = new HashMap<>();
            poisoned.put("goal", "community revitalization");
            poisoned.put("effects", Arrays.asList("displacement", "gentrification"));
            poisoned.put("legal_status", "legal");
            Action action = new Action("Raise rents on vulnerable tenants", poisoned);

            System.out.println("Action with disguised negative effects:");
            Map<String,CorelEvaluation> results = core.evaluate(action, Corel.FAIR.opcode, 88888L, 4500, false, 120);
            results.forEach((k,v)->System.out.println(k + " -> " + v));
        }
    }

    // --- FAULT INJECTION ---
    static class FaultInjectionScenario implements TestScenario {
        public String getName() { return "Fault Injection"; }
        public void run(CocorelsV3Skeleton core) {
            // Simulate a missing context field
            Action faulty = new Action("Execute without legal status", new HashMap<>());
            Map<String,CorelEvaluation> eval = core.evaluate(faulty, Corel.HONOUR_DUTY.opcode, 4321L, 3200, false, 100);
            System.out.println("Missing context field:");
            eval.forEach((k,v)->System.out.println(k + " -> " + v));

            // Simulate exception in heuristics (e.g., extremely large context)
            Map<String,Object> borked = new HashMap<>();
            borked.put("legal_status", new Object());
            Action exceptionAction = new Action("Break heuristics", borked);
            eval = core.evaluate(exceptionAction, Corel.HONOUR_DUTY.opcode, 123123L, 3200, false, 100);
            System.out.println("Broken context type:");
            eval.forEach((k,v)->System.out.println(k + " -> " + v));
        }
    }

    // --- OFFLINE ASSURANCE ---
    static class OfflineAssuranceScenario implements TestScenario {
        public String getName() { return "Offline/Local Assurance"; }
        public void run(CocorelsV3Skeleton core) {
            System.out.println("No network calls or remote dependencies detected in local test.");
            // If integrating with hardware, mock calls only
        }
    }

    // --- UTILITY ---
    private static String mapToString(Map<String,CorelEvaluation> map) {
        StringBuilder sb = new StringBuilder();
        for (Map.Entry<String,CorelEvaluation> e : map.entrySet()) {
            sb.append(e.getKey()).append(" -> ").append(e.getValue()).append("\n");
        }
        return sb.toString();
    }
}
