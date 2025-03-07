# -*- coding: utf-8 -*-
# TODO: break out into individual files under api/tests/die_roll
"""
Defines test case run against the API for DieRoll model
"""
from django.test import tag
from api.tests.base import RpgtApiBTC
from api.tests.base import ADMIN_USER
from api.tests.base import API_URL
from api.tests.base import RESPONSE_CODES
from api.tests.base import RO_USER
from api.tests.base import TOKEN_URL

MODEL_URL = API_URL + 'die-roll'

FIXTURES = ['test_users']

REQUEST_DATA_ZEROES = {
    "die_size": 0,
    "die_count": 0
}

REQUEST_DATA_ROLL_BASIC = {
    "die_size": 6,
    "die_count": 3
}

REQUEST_DATA_ROLL_MOD = {
    "die_size": 6,
    "die_count": 3,
    "roll_modifier": {
        "mod_type": "+",
        "value": 3
    }
}

REQUEST_DATA_PER_MOD = {
    "die_size": 6,
    "die_count": 3,
    "per_modifier": {
        "mod_type": "+",
        "value": 3
    }
}

REQUEST_DATA_POST_MOD = {
    "die_size": 6,
    "die_count": 3,
    "post_modifier": {
        "mod_type": "*",
        "value": 100
    }
}

REQUEST_DATA_PER_ROLL_MOD = {
    "die_size": 6,
    "die_count": 3,
    "per_modifier": {
        "mod_type": "+",
        "value": 1
    },
    "roll_modifier": {
        "mod_type": "+",
        "value": 3
    }
}

REQUEST_DATA_PER_POST_MOD = {
    "die_size": 6,
    "die_count": 3,
    "per_modifier": {
        "mod_type": "+",
        "value": 1
    },
    "post_modifier": {
        "mod_type": "*",
        "value": 10
    }
}

REQUEST_DATA_ROLL_POST_MOD = {
    "die_size": 6,
    "die_count": 3,
    "roll_modifier": {
        "mod_type": "+",
        "value": 3
    },
    "post_modifier": {
        "mod_type": "*",
        "value": 10
    }
}

REQUEST_DATA_PER_ROLL_POST_MOD = {
    "die_size": 6,
    "die_count": 3,
    "per_modifier": {
        "mod_type": "+",
        "value": 1
    },
    "roll_modifier": {
        "mod_type": "+",
        "value": 3
    },
    "post_modifier": {
        "mod_type": "*",
        "value": 10
    }
}

REQUEST_DATA_REROLL_EQ = {
    "die_size": 6,
    "die_count": 4,
    "roll_modifier": {
        "mod_type": "-",
        "value": 4
    },
    "reroll": {
        "value": 0,
        "condition": "=="
    }
}

REQUEST_DATA_REROLL_LTEQ = {
    "die_size": 6,
    "die_count": 4,
    "roll_modifier": {
        "mod_type": "-",
        "value": 10
    },
    "reroll": {
        "value": 0,
        "condition": "<="
    }
}

REQUEST_DATA_REROLL_LT = {
    "die_size": 6,
    "die_count": 4,
    "roll_modifier": {
        "mod_type": "-",
        "value": 10
    },
    "reroll": {
        "value": 1,
        "condition": "<"
    }
}

REQUEST_DATA_REROLL_GTEQ = {
    "die_size": 6,
    "die_count": 4,
    "roll_modifier": {
        "mod_type": "+",
        "value": 1
    },
    "reroll": {
        "value": 21,
        "condition": ">="
    }
}

REQUEST_DATA_REROLL_GT = {
    "die_size": 6,
    "die_count": 4,
    "roll_modifier": {
        "mod_type": "+",
        "value": 4
    },
    "reroll": {
        "value": 20,
        "condition": ">"
    }
}

REQUEST_DATA_ROLL_MOD_DIV = {
    "die_size": 6,
    "die_count": 4,
    "roll_modifier": {
        "mod_type": "/",
        "value": 2
    }
}

@tag("die_roll_admin")
class TestAdmin(RpgtApiBTC):
    """
    Defines die_roll test case class
    """
    fixtures = FIXTURES
    token = RpgtApiBTC.rpgu_api_cli.post(TOKEN_URL,
                                         ADMIN_USER,
                                         format="json").json()["access"]

    def test_post_zeroes(self):
        """
        Submits a POST request against MODEL_URL
        Validates admin access
        """
        response = self.rpgu_api_cli.post(MODEL_URL,
                                          REQUEST_DATA_ZEROES,
                                          format="json",
                                          HTTP_AUTHORIZATION=f"Bearer {self.token}")
        self.assertEqual(response.json()['roll'], 0)
        self.assertEqual(response.status_code, RESPONSE_CODES["created"])

@tag("die_roll_readonly")
class TestReadOnly(RpgtApiBTC):
    """
    Defines die_roll test case class
    """
    fixtures = FIXTURES
    token = RpgtApiBTC.rpgu_api_cli.post(TOKEN_URL,
                                         RO_USER,
                                         format="json").json()["access"]

    def test_post_zeroes(self):
        """
        Submits a POST request against MODEL_URL
        """
        response = self.rpgu_api_cli.post(MODEL_URL,
                                          REQUEST_DATA_ZEROES,
                                          format="json",
                                          HTTP_AUTHORIZATION=f"Bearer {self.token}")
        self.assertEqual(response.json()['roll'], 0)
        self.assertEqual(response.status_code, RESPONSE_CODES["created"])

@tag("die_roll_anonymous")
class TestAnonymous(RpgtApiBTC):
    """
    Defines die_roll test case class for anonymous access
    """

    def test_post_zeroes(self):
        """
        Submits a POST request against MODEL_URL
        """
        response = self.rpgu_api_cli.post(MODEL_URL,
                                          REQUEST_DATA_ZEROES,
                                          format="json")
        self.assertEqual(response.json()['roll'], 0)
        self.assertEqual(response.status_code, RESPONSE_CODES["created"])

    def test_post_basic(self):
        """
        Submits a POST request against MODEL_URL
        """
        response = self.rpgu_api_cli.post(MODEL_URL,
                                          REQUEST_DATA_ROLL_BASIC,
                                          format="json")
        self.assertGreaterEqual(response.json()['roll'], 3)
        self.assertLessEqual(response.json()['roll'], 18)
        self.assertEqual(response.status_code, RESPONSE_CODES["created"])

    def test_post_roll_mod(self):
        """
        Submits a POST request against MODEL_URL
        """
        response = self.rpgu_api_cli.post(MODEL_URL,
                                          REQUEST_DATA_ROLL_MOD,
                                          format="json")
        self.assertGreaterEqual(response.json()['roll'], 6)
        self.assertLessEqual(response.json()['roll'], 21)
        self.assertEqual(response.status_code, RESPONSE_CODES["created"])

    def test_post_per_mod(self):
        """
        Submits a POST request against MODEL_URL
        """
        response = self.rpgu_api_cli.post(MODEL_URL,
                                          REQUEST_DATA_PER_MOD,
                                          format="json")
        self.assertGreaterEqual(response.json()['roll'], 12)
        self.assertLessEqual(response.json()['roll'], 27)
        self.assertEqual(response.status_code, RESPONSE_CODES["created"])

    def test_post_post_mod(self):
        """
        Submits a POST request against MODEL_URL
        """
        response = self.rpgu_api_cli.post(MODEL_URL,
                                          REQUEST_DATA_POST_MOD,
                                          format="json")
        self.assertGreaterEqual(response.json()['roll'], 300)
        self.assertLessEqual(response.json()['roll'], 1800)
        self.assertEqual(response.status_code, RESPONSE_CODES["created"])

    def test_post_per_roll_mod(self):
        """
        Submits a POST request against MODEL_URL
        """
        response = self.rpgu_api_cli.post(MODEL_URL,
                                          REQUEST_DATA_PER_ROLL_MOD,
                                          format="json")
        self.assertGreaterEqual(response.json()['roll'], 9)
        self.assertLessEqual(response.json()['roll'], 24)
        self.assertEqual(response.status_code, RESPONSE_CODES["created"])

    def test_post_per_post_mod(self):
        """
        Submits a POST request against MODEL_URL
        """
        response = self.rpgu_api_cli.post(MODEL_URL,
                                          REQUEST_DATA_PER_POST_MOD,
                                          format="json")
        self.assertGreaterEqual(response.json()['roll'], 60)
        self.assertLessEqual(response.json()['roll'], 210)
        self.assertEqual(response.status_code, RESPONSE_CODES["created"])

    def test_post_roll_post_mod(self):
        """
        Submits a POST request against MODEL_URL
        """
        response = self.rpgu_api_cli.post(MODEL_URL,
                                          REQUEST_DATA_ROLL_POST_MOD,
                                          format="json")
        self.assertGreaterEqual(response.json()['roll'], 60)
        self.assertLessEqual(response.json()['roll'], 210)
        self.assertEqual(response.status_code, RESPONSE_CODES["created"])

    def test_post_per_roll_post_mod(self):
        """
        Submits a POST request against MODEL_URL
        """
        response = self.rpgu_api_cli.post(MODEL_URL,
                                          REQUEST_DATA_PER_ROLL_POST_MOD,
                                          format="json")
        self.assertGreaterEqual(response.json()['roll'], 90)
        self.assertLessEqual(response.json()['roll'], 240)
        self.assertEqual(response.status_code, RESPONSE_CODES["created"])

    def test_post_roll_mod_reroll_eq(self):
        """
        Submits a POST request against MODEL_URL
        """
        for iteration in range(2500):  # pylint: disable=unused-variable
            response = self.rpgu_api_cli.post(MODEL_URL,
                                              REQUEST_DATA_REROLL_EQ,
                                              format="json")
            self.assertGreaterEqual(response.json()['roll'], 1)
            self.assertLessEqual(response.json()['roll'], 20)
            self.assertEqual(response.status_code, RESPONSE_CODES["created"])

    def test_post_roll_mod_reroll_lteq(self):
        """
        Submits a POST request against MODEL_URL
        """
        for iteration in range(100):  # pylint: disable=unused-variable
            response = self.rpgu_api_cli.post(MODEL_URL,
                                              REQUEST_DATA_REROLL_LTEQ,
                                              format="json")
            self.assertGreaterEqual(response.json()['roll'], 1)
            self.assertLessEqual(response.json()['roll'], 20)
            self.assertEqual(response.status_code, RESPONSE_CODES["created"])

    def test_post_roll_mod_reroll_lt(self):
        """
        Submits a POST request against MODEL_URL
        """
        for iteration in range(100):  # pylint: disable=unused-variable
            response = self.rpgu_api_cli.post(MODEL_URL,
                                              REQUEST_DATA_REROLL_LT,
                                              format="json")
            self.assertGreaterEqual(response.json()['roll'], 1)
            self.assertLessEqual(response.json()['roll'], 20)
            self.assertEqual(response.status_code, RESPONSE_CODES["created"])

    def test_post_roll_mod_reroll_gteq(self):
        """
        Submits a POST request against MODEL_URL
        """
        for iteration in range(100):  # pylint: disable=unused-variable
            response = self.rpgu_api_cli.post(MODEL_URL,
                                              REQUEST_DATA_REROLL_GTEQ,
                                              format="json")
            self.assertGreaterEqual(response.json()['roll'], 1)
            self.assertLessEqual(response.json()['roll'], 20)
            self.assertEqual(response.status_code, RESPONSE_CODES["created"])

    def test_post_roll_mod_reroll_gt(self):
        """
        Submits a POST request against MODEL_URL
        """
        for iteration in range(100):  # pylint: disable=unused-variable
            response = self.rpgu_api_cli.post(MODEL_URL,
                                              REQUEST_DATA_REROLL_GT,
                                              format="json")
            self.assertGreaterEqual(response.json()['roll'], 1)
            self.assertLessEqual(response.json()['roll'], 20)
            self.assertEqual(response.status_code, RESPONSE_CODES["created"])

    def test_post_roll_mod_div(self):
        """
        Submits a POST request against MODEL_URL
        """
        for iteration in range(100):  # pylint: disable=unused-variable
            response = self.rpgu_api_cli.post(MODEL_URL,
                                              REQUEST_DATA_ROLL_MOD_DIV,
                                              format="json")
            self.assertEqual(type(response.json()['roll']), type(1))
            self.assertEqual(response.status_code, RESPONSE_CODES["created"])
