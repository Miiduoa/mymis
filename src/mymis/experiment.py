from math import erf, sqrt

def _phi(z: float) -> float:
    return 0.5 * (1 + erf(z / sqrt(2)))

def compare_binary(control_success, control_total, variant_success, variant_total):
    if min(control_total, variant_total) <= 0:
        raise ValueError("totals must be positive")
    pc = control_success / control_total
    pv = variant_success / variant_total
    pooled = (control_success + variant_success) / (control_total + variant_total)
    se = sqrt(max(pooled * (1 - pooled) * (1/control_total + 1/variant_total), 1e-15))
    z = (pv - pc) / se
    p = 2 * (1 - _phi(abs(z)))
    return {
        "control_rate": pc,
        "variant_rate": pv,
        "absolute_lift": pv - pc,
        "relative_lift": (pv - pc) / pc if pc else None,
        "z": z,
        "p_value": p,
    }

def sample_ratio_mismatch(control_total, variant_total, expected_share=0.5):
    total = control_total + variant_total
    expected_c = total * expected_share
    expected_v = total * (1 - expected_share)
    chi2 = ((control_total - expected_c) ** 2 / expected_c) + ((variant_total - expected_v) ** 2 / expected_v)
    p = 1 - erf(sqrt(chi2 / 2))
    return {"chi2": chi2, "p_value": p, "flag": p < 0.01}
