from math import erf, sqrt
from statistics import NormalDist


def _phi(z: float) -> float:
    return 0.5 * (1 + erf(z / sqrt(2)))


def compare_binary(control_success, control_total, variant_success, variant_total, confidence=0.95):
    if min(control_total, variant_total) <= 0:
        raise ValueError("totals must be positive")
    if not (0 <= control_success <= control_total and 0 <= variant_success <= variant_total):
        raise ValueError("successes must be between 0 and total")
    if not 0 < confidence < 1:
        raise ValueError("confidence must be between 0 and 1")

    pc = control_success / control_total
    pv = variant_success / variant_total
    pooled = (control_success + variant_success) / (control_total + variant_total)
    pooled_se = sqrt(max(pooled * (1 - pooled) * (1 / control_total + 1 / variant_total), 1e-15))
    z = (pv - pc) / pooled_se
    p = 2 * (1 - _phi(abs(z)))

    diff = pv - pc
    diff_se = sqrt(
        max(
            pc * (1 - pc) / control_total + pv * (1 - pv) / variant_total,
            1e-15,
        )
    )
    z_critical = NormalDist().inv_cdf(1 - (1 - confidence) / 2)

    return {
        "control_rate": pc,
        "variant_rate": pv,
        "absolute_lift": diff,
        "relative_lift": diff / pc if pc else None,
        "z": z,
        "p_value": p,
        "confidence": confidence,
        "absolute_lift_ci": (
            diff - z_critical * diff_se,
            diff + z_critical * diff_se,
        ),
    }


def sample_ratio_mismatch(control_total, variant_total, expected_share=0.5):
    if min(control_total, variant_total) < 0:
        raise ValueError("totals cannot be negative")
    if control_total + variant_total <= 0:
        raise ValueError("combined total must be positive")
    if not 0 < expected_share < 1:
        raise ValueError("expected_share must be between 0 and 1")

    total = control_total + variant_total
    expected_c = total * expected_share
    expected_v = total * (1 - expected_share)
    chi2 = ((control_total - expected_c) ** 2 / expected_c) + ((variant_total - expected_v) ** 2 / expected_v)
    p = 1 - erf(sqrt(chi2 / 2))
    return {"chi2": chi2, "p_value": p, "flag": p < 0.01}


def minimum_detectable_lift(base_rate, samples_per_group, alpha=0.05, power=0.8):
    """Approximate absolute MDE for equal-sized binary experiments."""
    if not 0 < base_rate < 1:
        raise ValueError("base_rate must be between 0 and 1")
    if samples_per_group <= 0:
        raise ValueError("samples_per_group must be positive")
    if not 0 < alpha < 1 or not 0 < power < 1:
        raise ValueError("alpha and power must be between 0 and 1")

    normal = NormalDist()
    z_alpha = normal.inv_cdf(1 - alpha / 2)
    z_power = normal.inv_cdf(power)
    standard_error = sqrt(2 * base_rate * (1 - base_rate) / samples_per_group)
    return (z_alpha + z_power) * standard_error
