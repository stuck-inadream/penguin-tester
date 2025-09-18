def evaluate_ckmm_pass(fuel, temporal, council, ethics, substrate, thresholds):
    # Fuel
    fuel_ok = (fuel.get("wall_s",0) <= thresholds["fuel"]["max_time_s"] and
               fuel.get("kib",0) <= thresholds["fuel"]["max_kib"] and
               fuel.get("attention_ticks",0) <= thresholds["fuel"]["max_attention"])

    # Temporal
    stable_ok = temporal.get("stability",0) >= thresholds["temporal"]["stability_min"]

    # Council (plus weighted illustrative metric)
    agreement = council.get("agreement", 0.0)
    council_ok = agreement >= thresholds["relational"]["council_min"]
    weighted_agreement = agreement * 1.5
    weighted_council_ok = weighted_agreement >= thresholds["relational"]["council_min"]

    # Ethics
    ethics_ok = (ethics.get("penalty",0) <= thresholds["ethics"]["max_penalty"] and
                 (1.0 if ethics.get("recovered") else 0.0) >= thresholds["ethics"]["recovery_min"])

    substrate_ok = True  # placeholder interface

    return {
        "fuel_ok": fuel_ok,
        "stable_ok": stable_ok,
        "council_ok": council_ok,
        "weighted_council_ok": weighted_council_ok,
        "ethics_ok": ethics_ok,
        "substrate_ok": substrate_ok,
        "all_ok": fuel_ok and stable_ok and (council_ok or weighted_council_ok) and ethics_ok and substrate_ok
    }
