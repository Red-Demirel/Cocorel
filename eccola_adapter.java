public class EccolaCorelsAdapter implements EthicalDecisionGateway {
    private final CocorelsV3Skeleton core;
    private final BrassCardRegistry brassRegistry;

    public EccolaCorelsAdapter(EccolaSystem eccola) {
        this.core = new CocorelsV3Skeleton(loadConfig());
        this.brassRegistry = eccola.getBrassCardService();
    }

    public EthicalVerdict evaluateAction(Action action) {
        // Calculate complexity score from Eccola's context
        int complexity = eccola.calculateComplexity(action); 
        
        // Perform Corels evaluation
        Map<String,CorelEvaluation> eval = core.evaluate(
            action, 
            Corel.FAIRNESS.opcode,
            action.hash64(),
            complexity,
            false,
            100
        );

        // Apply Brass Card reputation weighting
        double weightedScore = brassRegistry.applyReputationWeighting(eval);
        
        return new EthicalVerdict(weightedScore, eval);
    }

    // Auto-configuration from Eccola environment
    private Map<String,Object> loadConfig() {
        Map<String,Object> cfg = new HashMap<>();
        cfg.put("eccola_mode", true);
        cfg.put("brass_integration", true);
        return cfg;
    }
}