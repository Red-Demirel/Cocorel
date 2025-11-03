class GrokCoCorelsAdapter:
    def __init__(self, core_engine):
        self.engine = core_engine
        self.cache = {}
    
    def process(self, query, context):
        # Ethical pre-filter with 5ms timeout
        if not self.engine.is_ethical_query(query, context):
            return None  # Bypass to standard Grok
        
        # Process with CoCorels
        report = self.engine.process_ethical_dilemma(query, context)
        
        if report.get("status") == "Request clarification":
            return self._format_clarification(report)
        
        return self._format_output(report)
    
    def _format_output(self, report):
        return {
            "ethical_score": report["final_mcda_score"],
            "corels_trace": self._simplify_trace(report),
            "balance_alert": report["balance_score"] > 25
        }
    
    def _simplify_trace(self, report):
        return {k: v for k, v in report["scores"].items() if v < 15000}