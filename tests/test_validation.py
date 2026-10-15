import unittest

from campusflow.validation import (
    ValidationError,
    check_affected_users,
    check_category,
    check_staff_name,
    check_title,
    check_urgency,
)


class TestAffectedUsers(unittest.TestCase):
    def test_accepts_positive_integer(self):
        self.assertEqual(check_affected_users(5), 5)

    def test_rejects_zero_and_negative_numbers(self):
        for value in (0, -3):
            with self.subTest(value=value):
                with self.assertRaises(ValidationError):
                    check_affected_users(value)

    def test_rejects_float(self):
        with self.assertRaises(ValidationError):
            check_affected_users(2.5)

    def test_rejects_numeric_string(self):
        with self.assertRaises(ValidationError):
            check_affected_users("5")

    def test_rejects_boolean_even_though_bool_is_an_int(self):
        # isinstance(True, int) is True, so a plain isinstance check
        # would wrongly accept True as "1 affected user".
        for value in (True, False):
            with self.subTest(value=value):
                with self.assertRaises(ValidationError):
                    check_affected_users(value)


class TestCategory(unittest.TestCase):
    def test_normalizes_case_and_whitespace_to_canonical_value(self):
        self.assertEqual(check_category("  nEtWoRk "), "Network")

    def test_accepts_every_allowed_category(self):
        for category in ("Network", "Hardware", "Software", "Other"):
            with self.subTest(category=category):
                self.assertEqual(check_category(category.lower()), category)

    def test_rejects_unknown_category(self):
        with self.assertRaises(ValidationError):
            check_category("Printer")

    def test_rejects_non_text_category(self):
        with self.assertRaises(ValidationError):
            check_category(None)


class TestUrgency(unittest.TestCase):
    def test_normalizes_case(self):
        self.assertEqual(check_urgency("HIGH"), "high")

    def test_rejects_unknown_urgency(self):
        with self.assertRaises(ValidationError):
            check_urgency("urgent")

    def test_rejects_blank_urgency(self):
        with self.assertRaises(ValidationError):
            check_urgency("   ")


class TestTitle(unittest.TestCase):
    def test_trims_surrounding_whitespace(self):
        self.assertEqual(check_title("  Wi-Fi down "), "Wi-Fi down")

    def test_rejects_blank_title(self):
        for title in ("", "   "):
            with self.subTest(title=title):
                with self.assertRaises(ValidationError):
                    check_title(title)

    def test_rejects_non_text_title(self):
        with self.assertRaises(ValidationError):
            check_title(123)


class TestStaffName(unittest.TestCase):
    def test_trims_staff_name(self):
        self.assertEqual(check_staff_name("  Ada "), "Ada")

    def test_rejects_blank_staff_name(self):
        for name in ("", "   "):
            with self.subTest(name=name):
                with self.assertRaises(ValidationError):
                    check_staff_name(name)

    def test_rejects_none_staff_name(self):
        with self.assertRaises(ValidationError):
            check_staff_name(None)

    def test_validation_error_is_a_value_error(self):
        # Keeps existing `except ValueError` handlers in main.py working.
        self.assertTrue(issubclass(ValidationError, ValueError))


if __name__ == "__main__":
    unittest.main()