def estimate_runtime_by_appliance(appliances, total_energy_consumption: int):
    appliances_per_category = {category: list(category_appliances) for category, category_appliances in group_by_category(appliances)}

    smallest_rest = total_energy_consumption
    maximized_runtime_per_category = None

    for available_categories in [appliances_per_category]:
        print('running for', available_categories)
        runtime_per_category, rest = maximize_runtime_per_category(
            available_categories,
            {category: DAILY_TOTAL_OPERATING_HOURS_RANGE_BY_CATEGORY[category].min / len(category_appliances) for category, category_appliances in appliances_per_category.items()},
            appliances_per_category,
            total_energy_consumption
        )

        if rest < smallest_rest:
            smallest_rest = rest
            maximized_runtime_per_category = runtime_per_category

    return {
        appliance: maximized_runtime_per_category[appliance.category]
        for appliance in appliances
    }

def maximize_runtime_per_category(available_categories, runtime_per_category, appliances_per_category, total_energy_consumption):
    # we're looking for the set of runtimes that maximizes E{F} + E{A} + E{T} while staying lower than total_energy_consumption
    smallest_rest = total_energy_consumption
    maximized_runtime_per_category = runtime_per_category

    print(' ' * (3 - len(available_categories)), runtime_per_category)

    x = Symbol('x')

    for category in available_categories:
        appliances = appliances_per_category[category]
        # how many times 
        total_other_categories = sum(sum(appliance.power * runtime for appliance in appliances_per_category[other_cat]) for other_cat, runtime in runtime_per_category.items() if other_cat != category)

        usable_energy_for_category = total_energy_consumption - total_other_categories

        max_fit = min(
            int(solve(Eq(sum(appliance.power * x / len(appliances) for appliance in appliances), usable_energy_for_category), x)[0]),
            DAILY_TOTAL_OPERATING_HOURS_RANGE_BY_CATEGORY[category].max
        ) / len(appliances)

        rest = usable_energy_for_category - sum(appliance.power * max_fit for appliance in appliances)

        print(' ' * (3 - len(available_categories)), category, ": total_other_categories", total_other_categories, "max_fit", max_fit, "rest", rest)

        runtime_per_category_with_new_max_for_current_category = dict(runtime_per_category)
        runtime_per_category_with_new_max_for_current_category[category] = max_fit

        if rest == 0:
            return runtime_per_category_with_new_max_for_current_category, 0
        elif len(available_categories) > 1:
            available_categories_without_current_category = [other_cat for other_cat in available_categories if other_cat != category]
            print(' ' * (3 - len(available_categories)), 'recurse for', available_categories_without_current_category)
            nested_runtime_per_category, nested_rest = maximize_runtime_per_category(available_categories_without_current_category, runtime_per_category_with_new_max_for_current_category, appliances_per_category, total_energy_consumption)
            if nested_rest < rest:
                print(' ' * (3 - len(available_categories)), 'found smaller rest in recursion', nested_rest)
                rest = nested_rest
                runtime_per_category_with_new_max_for_current_category = nested_runtime_per_category

        if rest < smallest_rest:
            print(' ' * (3 - len(available_categories)), 'found smaller rest', rest)
            smallest_rest = rest
            maximized_runtime_per_category =  runtime_per_category_with_new_max_for_current_category

    return maximized_runtime_per_category, smallest_rest
