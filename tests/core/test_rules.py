from dataclasses import dataclass

import pytest

from energy_app.core import rules


@dataclass(eq=True, frozen=True)
class MockCategory:
    name: str
    minimum_operating_hours: int
    maximum_operating_hours: int


@pytest.fixture
def cat_f():
    return MockCategory(name="F", minimum_operating_hours=6, maximum_operating_hours=8)


@pytest.fixture
def cat_a():
    return MockCategory(name="A", minimum_operating_hours=1, maximum_operating_hours=4)


@pytest.fixture
def cat_l():
    return MockCategory(name="L", minimum_operating_hours=4, maximum_operating_hours=24)


@dataclass(eq=True, frozen=True)
class MockAppliance:
    power: int
    category: str


@pytest.fixture
def fridge(cat_f):
    return MockAppliance(power=2000, category=cat_f)


@pytest.fixture
def freezer(cat_f):
    return MockAppliance(power=2500, category=cat_f)


@pytest.fixture
def dishwasher(cat_a):
    return MockAppliance(power=2500, category=cat_a)


@pytest.fixture
def small_light(cat_l):
    return MockAppliance(power=100, category=cat_l)


@pytest.fixture
def big_light(cat_l):
    return MockAppliance(power=800, category=cat_l)


def test_minimal_total_consumption(fridge, dishwasher, small_light, big_light):
    assert rules.minimal_total_consumption([fridge, dishwasher, small_light]) == 2000 * 6 + 2500 * 1 + 100 * 4
    assert rules.minimal_total_consumption([dishwasher, big_light]) == 2500 * 1 + 800 * 4
    assert rules.minimal_total_consumption([small_light, big_light]) == (100 + 800) * 4
    assert rules.minimal_total_consumption([fridge, big_light, dishwasher, small_light]) == 2000 * 6 + 2500 * 1 + (800 + 100) * 4


def test_estimate_runtime_by_appliance(fridge, freezer, dishwasher, small_light, big_light):
    # simple case, we have a case where rest is 0
    assert rules.estimate_runtime_by_appliance([fridge, freezer, small_light, big_light], 28_800) == {
        fridge: 4,
        freezer: 4,
        small_light: 12,
        big_light: 12
    }

    # more complex case, 
    assert rules.estimate_runtime_by_appliance([fridge, dishwasher, small_light, big_light], 20_200) == {
        fridge: 6,
        dishwasher: 2,
        small_light: 3.5,
        big_light: 3.5
    }
