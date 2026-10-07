def check_guardrails(metrics):
    results = []
    for metric in metrics:
        name = metric["name"]
        control = float(metric["control"])
        variant = float(metric["variant"])
        tolerance = float(metric.get("tolerance", 0))
        mode = metric.get("mode", "min")
        if mode not in {"min", "max"}:
            raise ValueError("guardrail mode must be 'min' or 'max'")
        if tolerance < 0:
            raise ValueError("guardrail tolerance cannot be negative")
        if control == 0:
            raise ValueError(f"guardrail {name} requires non-zero control value")
        relative_change = (variant - control) / abs(control)
        breached = relative_change < -tolerance if mode == "min" else relative_change > tolerance
        results.append({"name": name, "relative_change": relative_change, "tolerance": tolerance, "mode": mode, "breached": breached})
    return results


def experiment_decision(primary_result, srm_result, guardrail_results, alpha=0.05):
    if srm_result.get("flag"):
        return {"decision": "invalid", "reason": "sample ratio mismatch"}
    breached = [row["name"] for row in guardrail_results if row.get("breached")]
    if breached:
        return {"decision": "hold", "reason": "guardrail breach: " + ", ".join(breached)}
    p_value = primary_result["p_value"]
    lift = primary_result["absolute_lift"]
    if p_value < alpha and lift > 0:
        return {"decision": "ship", "reason": "positive primary metric with no guardrail breach"}
    if p_value < alpha and lift < 0:
        return {"decision": "reject", "reason": "significant negative primary metric"}
    return {"decision": "inconclusive", "reason": "primary metric is not statistically decisive"}
