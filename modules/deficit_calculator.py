daily_deficit_for_1_kg_in_a_week = 1111 # kcal
kg_to_kcal = 7777

def daily_deficit_for_weeks(target_weight: float, current_weight: float, weeks_until_target: float):
    kg_to_lose = current_weight - target_weight
    kg_to_lose_per_week = kg_to_lose / weeks_until_target
    daily_deficit = kg_to_lose_per_week * daily_deficit_for_1_kg_in_a_week
    return daily_deficit

def weeks_given_daily_deficit(target_weight: float, current_weight: float, daily_deficit: float):
    kg_to_lose = current_weight - target_weight
    total_kcal_to_lose = kg_to_lose*kg_to_kcal
    days = total_kcal_to_lose/daily_deficit
    return days/7


target_weight = 80
current_weight = 95
weeks_until_target = 21
daily_deficit = 500


print(daily_deficit_for_weeks(target_weight, current_weight, weeks_until_target))
# print(weeks_given_daily_deficit(target_weight, current_weight, daily_deficit))

# Moderately active adult:
# - Male:   2600 kcal / day
# - Female: 2100 kcal / day