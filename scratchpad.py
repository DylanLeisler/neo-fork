"""Compare original level-based damage against the new domain/stat-based model."""

domain_stat_weights = {
    "Concentration": {
        "Atk": 3,
        "Def": 3,
        "SpAtk": 4,
        "SpDef": 6,
        "Spd": 1,
    },
    "Flow": {
        "Atk": 3,
        "Def": 3,
        "SpAtk": 2,
        "SpDef": 2,
        "Spd": 7,
    },
    "Power": {
        "Atk": 6,
        "Def": 3,
        "SpAtk": 2,
        "SpDef": 3,
        "Spd": 3,
    },
    "Longevity": {
        "Atk": 2,
        "Def": 6,
        "SpAtk": 2,
        "SpDef": 4,
        "Spd": 3,
    },
    "Presence": {
        "Atk": 3,
        "Def": 2,
        "SpAtk": 7,
        "SpDef": 2,
        "Spd": 3,
    },
}

def org_dmg_formula(level, power, att, defense):
    """Original base damage formula."""
    return (((((2 * level) / 5 + 2) * power * att / defense) / 50) + 2)


def get_single_stat_one_weight(level, max_possible_level, weight, base_stat: int, IV, nature):
    """Custom non-HP stat approximation for a single weighted domain contribution."""
    base_term = 2 * base_stat + IV # hardcoded '2' is inherited from original form.
    ev_replacement_multi = 3 # this essentially embeds the impact of EVs into domains.
    domain_multi = 3
    domain_term = domain_multi * ev_replacement_multi * weight * level
    scaled_total = (base_term + domain_term) * 2 / max_possible_level
    offset = 15
    return (scaled_total - offset) * nature

def get_single_stat_all_weights(level_profile, max_possible_level, base_stat: tuple, IV, nature, key_ord):
    """Compute one stat from a domain profile snapshot."""
    # Convert domain progress into an EV-like aggregate using per-domain stat weights.
    total_weighted_level = sum(
        level * domain_stat_weights[key][base_stat[0].capitalize()]
        for level, key in zip(level_profile, key_ord)
    )
    # Apply the custom stat formula once using the aggregated weighted contribution.
    return ((2 * base_stat[1] + IV + 9 * total_weighted_level) / (max_possible_level / 2) - 15) * nature


def new_dmg_formula(c_slope, c_floor, power, att, defense):
    """New damage formula where growth comes from attack-derived c, not total level."""
    return get_damage_constant(c_slope, c_floor, att) * power * att / defense + 2

def get_damage_constant(slope, floor_point, attack):
    """Map attack to c using a floor anchor and slope."""
    return floor_point[0] + slope * (attack - floor_point[1])


def get_damage_constant_slope(mapping):
    """Compute c-vs-attack slope from floor/ceil anchor points."""
    floor = mapping["floor"]
    ceil = mapping["ceil"]
    return (ceil[0] - floor[0]) / (ceil[1] - floor[1])


def get_scaled_domain_profile(full_profile, checkpoint, max_checkpoint):
    """Scale full domain levels to a checkpoint ratio and round each domain level."""
    scale = checkpoint / max_checkpoint
    return [round(level * scale) for level in full_profile]


def resolve_stat_by_checkpoint(stat_value, levels):
    """Return one base stat value per checkpoint level."""
    if isinstance(stat_value, (int, float)):
        return [stat_value for _ in levels]
    if isinstance(stat_value, (list, tuple)):
        if len(stat_value) != len(levels):
            raise ValueError(f"Expected {len(levels)} base stat values, got {len(stat_value)}")
        return list(stat_value)
    raise TypeError("Base stat must be int/float or a list/tuple of per-checkpoint values")


def print_damage_comparison(
    levels, old_formula_levels, domain_profiles, base_atk_by_level, base_def_by_level, atk_by_level, defense_by_level, org_dmg, new_dmg
):
    """Render a compact comparison table for quick visual inspection."""
    header = (
        f"{'Chk':>4} {'OldLvl':>7} {'DomainProfile':>21} {'DSum':>6} {'BaseAtk':>8} {'BaseDef':>8} "
        f"{'Atk':>10} {'Def':>10} {'Original':>10} {'New':>10} {'Delta':>10} {'%Delta':>9}"
    )
    print(header)
    print("-" * len(header))
    for checkpoint, old_level, profile, base_atk, base_def, atk, defense, org, new in zip(
        levels, old_formula_levels, domain_profiles, base_atk_by_level, base_def_by_level, atk_by_level, defense_by_level, org_dmg, new_dmg
    ):
        domain_sum = sum(profile)
        delta = new - org
        pct_delta = (delta / org * 100) if org else 0.0
        print(
            f"{checkpoint:>4} {old_level:>7} {str(profile):>21} {domain_sum:>6} {base_atk:>8.1f} {base_def:>8.1f} "
            f"{atk:>10.2f} {defense:>10.2f} {org:>10.2f} {new:>10.2f} {delta:>10.2f} {pct_delta:>8.2f}%"
        )

            

def main():
    """Build snapshots and compare old level-scaling damage to new attack-driven damage."""
    levels = [5, 10, 15, 20]
    max_level = 20
    move_powers = [10, 35, 50, 90, 130]
    nature_mult = 1
    base_stats = {
        "atk": [53,91,135,180],
        "def": [54,92,136,181]
    }
    max_IV = 31
    domain_stat_weight_key_order = ["Concentration", "Flow", "Power", "Longevity", "Presence"]
    demo_domain_profile = [5, 8, 15, 8, 4]
    damage_constant_to_attack_mapping = {
        "floor": [0.048, 6],
        "ceil": [0.84, 192],
    }

    max_checkpoint = max(levels)
    base_atk_by_level = resolve_stat_by_checkpoint(base_stats["atk"], levels)
    base_def_by_level = resolve_stat_by_checkpoint(base_stats["def"], levels)
    domain_profiles = [get_scaled_domain_profile(demo_domain_profile, level, max_checkpoint) for level in levels]
    atk_by_level = [
        get_single_stat_all_weights(profile, max_level, ("atk", base_atk), max_IV, nature_mult, domain_stat_weight_key_order)
        for profile, base_atk in zip(domain_profiles, base_atk_by_level)
    ]
    defense_by_level = [
        get_single_stat_all_weights(profile, max_level, ("def", base_def), max_IV, nature_mult, domain_stat_weight_key_order)
        for profile, base_def in zip(domain_profiles, base_def_by_level)
    ]

    org_dmg = []
    new_dmg = []
    old_formula_levels = [level * 5 for level in levels]
    damage_constant_slope = get_damage_constant_slope(damage_constant_to_attack_mapping)
    damage_constant_floor = damage_constant_to_attack_mapping["floor"]

    for old_level, profile, base_atk, base_def, atk, defense in zip(
        old_formula_levels, domain_profiles, base_atk_by_level, base_def_by_level, atk_by_level, defense_by_level
    ):
        org_dmg.append(org_dmg_formula(old_level, move_powers[3], base_atk, base_def))
        new_dmg.append(
            new_dmg_formula(damage_constant_slope, damage_constant_floor, move_powers[3], atk, defense)
        )

    print("Damage Comparison (move power = 90)")
    print(f"Full domain profile at checkpoint {max_checkpoint}: {demo_domain_profile}")
    print_damage_comparison(
        levels, old_formula_levels, domain_profiles, base_atk_by_level, base_def_by_level, atk_by_level, defense_by_level, org_dmg, new_dmg
    )



if __name__ == "__main__":
    main()
