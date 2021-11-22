# This file is part product_cost_invisible module for Tryton.
# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.
import unittest


from trytond.tests.test_tryton import ModuleTestCase
from trytond.tests.test_tryton import suite as test_suite


class ProductCostInvisibleTestCase(ModuleTestCase):
    'Test Product Cost Invisible module'
    module = 'product_cost_invisible'


def suite():
    suite = test_suite()
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(
            ProductCostInvisibleTestCase))
    return suite
