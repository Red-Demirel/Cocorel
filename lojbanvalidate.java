public static boolean lojbanValidate(String lojbanPredicate, Map<String,Object> context) {
    // Maps to ECCOLA’s non-maleficence for open societies
    return lojbanPredicate.contains("no_harm") && !context.getOrDefault("harm_risk", false);
}