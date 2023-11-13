from itertools import groupby

from optlang import Model, Variable, Constraint, Objective


MAXIMUM_TOTAL_DAILY_CONSUMPTION = 75_000


def group_by_category(appliances):
    def category_getter(appliance):
        return appliance.category

    return groupby(sorted(appliances, key=lambda c: c.category.name), key=category_getter)


def minimal_total_consumption(appliances) -> int:
    # Return minimal daily consumption for a set of appliances
    # Note that the operating range for a given category is for the total of the appliances in the category
    # not each appliance in the category
    # that's why we sum by category before multiplying by the minimal operating hours of the category
    return sum(
        sum(appliance.power for appliance in category_appliances) * category.minimum_operating_hours
        for category, category_appliances in group_by_category(appliances)
    )


def estimate_runtime_by_appliance(appliances, total_energy_consumption: int):
    appliances_per_category = {category: list(category_appliances) for category, category_appliances in group_by_category(appliances)}

    # Let's say we have a fridge (2000W, cat F), a freezer (2500W, cat F), a dishwasher (2500W, cat A),
    # a big light (800W, cat L) and small light (100W, cat L)
    # We want to solve the "main equation": 2000 x rF1 + 2500 x rF2 + 2500 x rA2 + 800 x rL1 + 100 x rL2 <= total_energy_consumption
    # where:
    # A) rF1 = rF2 and rL1 = rL2
    # B) rF1 + rF2 is an integer between 6 and 8, rA2 is an integer between 1 and 4, rL1 + rL2 is an integer between 1 and 24
    # Thanks to A we can introduce rF where rF1 = rF / 2, rF2 = rF / 2; then rA where rA1 = rA; finally rL where rL1 = rL / 2 and rL2 = rL / 2
    # so we can simplify the main equation to (2000 + 2500) * rF / 2 + 2500 * rA + (800 + 100) * rL / 2 <= total_energy_consumption
    # All of this translates nicely to an optimization problem where we try to maximize the function (2000 + 2500) * rF / 2 + 2500 * rA + (800 + 100) * rL / 2, with an upper bound for the function the main equation and for rF, rA and rF from B)

    variables = {
        category: Variable(
            category.name,
            lb=category.minimum_operating_hours,
            ub=category.maximum_operating_hours,
            type='integer'
        )
        for category, appliances in appliances_per_category.items()
    }

    total_equation = sum(
        sum(appliance.power for appliance in appliances) * variables[category] / len(appliances)
        for category, appliances in appliances_per_category.items())

    model = Model('runtime')
    model.objective = Objective(total_equation, direction='max')
    model.add([Constraint(total_equation, ub=total_energy_consumption)])
    model.optimize()

    return {
        appliance: model.variables[appliance.category.name].primal / len(appliances_per_category[appliance.category])
        for appliance in appliances
    }
