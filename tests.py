import unittest

from Character import Warrior


class TestWarrior(unittest.TestCase):

    def setUp(self):

        self.warrior = Warrior("TestWarrior", 30, "Male", 80, 180, "test@warrior.com")

    def test_initial_values(self):

        self.assertEqual(self.warrior.get_name(), "TestWarrior")
        self.assertEqual(self.warrior.get_health(), 0)  # Так как health_calculator зависит от других значений
        self.assertEqual(self.warrior.get_damage(), 0)  # Так как damage_calculator зависит от других значений
        self.assertEqual(self.warrior.get_heal_amount(), 0)  # heal_calculator также зависит от других значений
        self.assertEqual(self.warrior.get_email(), "test@warrior.com")

    def test_health_calculator(self):
        self.warrior._progress.set_xp(100)
        self.warrior.set_hydration(3)
        self.warrior.set_sleep_time(6)
        self.warrior.health_calculator()

        expected_health = (self.warrior._progress.get_level() + (50 * (3 + 6)))
        self.assertEqual(self.warrior.get_health(), expected_health)

    def test_damage_calculator(self):

        self.warrior.set_hydration(3)
        self.warrior.set_sleep_time(6)
        self.warrior.damage_calculator()

        expected_damage = pow(self.warrior._progress.get_level(), (6 / 4 + 3 / 2))
        self.assertEqual(self.warrior.get_damage(), round(expected_damage, 0))

    def test_heal_calculator(self):

        self.warrior.heal_calculator()
        expected_heal_amount = self.warrior._progress.get_level() * 5
        self.assertEqual(self.warrior.get_heal_amount(), expected_heal_amount)

    def test_set_and_get_email(self):

        self.warrior.set_email("newemail@warrior.com")
        self.assertEqual(self.warrior.get_email(), "newemail@warrior.com")

    def test_set_sleep_time(self):

        self.warrior.set_sleep_time(10)
        self.assertEqual(self.warrior._sleep_time, 8)

    def test_set_hydration(self):

        self.warrior.set_hydration(6)
        self.assertEqual(self.warrior._hydration, 5)

    def test_change_name(self):

        self.warrior.change_name("NewWarrior", 1)
        self.assertEqual(self.warrior.get_name(), "NewWarrior")


if __name__ == "__main__":
    unittest.main()

