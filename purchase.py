# This file is part product_cost_invisible module for Tryton.
# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.
from trytond.pool import PoolMeta, Pool
from trytond.transaction import Transaction
from decimal import Decimal
from trytond.modules.product_cost_invisible.product import PYSON_STATEMENT


class Purchase(metaclass=PoolMeta):
    __name__ = 'purchase.purchase'

    @classmethod
    def __setup__(cls):
        super().__setup__()
        cls.untaxed_amount.states['invisible'] = PYSON_STATEMENT
        cls.tax_amount.states['invisible'] = PYSON_STATEMENT
        cls.total_amount.states['invisible'] = PYSON_STATEMENT

    @classmethod
    def view_attributes(cls):
        pool = Pool()
        Data = pool.get('ir.model.data')

        groups = Transaction().context.get('groups', [])
        product_cost_invisible_admin_group = Data.get_id(
            'product_cost_invisible', 'group_product_cost_invisible_admin')
        not_allowed_user = product_cost_invisible_admin_group not in groups
        return super().view_attributes() + [
            ('/tree/field[@name="untaxed_amount"]', 'tree_invisible',
                not_allowed_user)]


class PurchaseLine(metaclass=PoolMeta):
    __name__ = 'purchase.line'

    @classmethod
    def __setup__(cls):
        super().__setup__()
        cls.amount.states['invisible'] = PYSON_STATEMENT
        cls.taxes.states['invisible'] = PYSON_STATEMENT

    @classmethod
    def is_allowed_user(cls):
        pool = Pool()
        Data = pool.get('ir.model.data')

        transaction = Transaction()
        if transaction.user == 0:
            return True

        groups = transaction.context.get('groups', [])
        product_cost_invisible_admin_group = Data.get_id(
            'product_cost_invisible', 'group_product_cost_invisible_admin')
        return product_cost_invisible_admin_group in groups

    @classmethod
    def view_attributes(cls):
        not_allowed_user = not cls.is_allowed_user()
        return super().view_attributes() + [
            ('/tree/field[@name="unit_price"]', 'tree_invisible',
                not_allowed_user),
            ('/tree/field[@name="amount"]', 'tree_invisible',
                not_allowed_user),
            ('/tree/field[@name="taxes"]', 'tree_invisible',
                not_allowed_user),
            ]

    def compute_base_price(self):
        if not self.is_allowed_user():
            return
        return super().compute_base_price()

    def on_change_product(self):
        super().on_change_product()
        if not self.is_allowed_user():
            self.unit_price = Decimal(0)

    def on_change_quantity(self):
        pool = Pool()
        Data = pool.get('ir.model.data')

        groups = Transaction().context.get('groups', [])
        product_cost_invisible_admin_group = Data.get_id(
            'product_cost_invisible', 'group_product_cost_invisible_admin')
        not_allowed_user = product_cost_invisible_admin_group not in groups
        super().on_change_quantity()
        if not_allowed_user:
            self.unit_price = Decimal(0)


class ProductSupplier(metaclass=PoolMeta):
    __name__ = 'purchase.product_supplier'

    @classmethod
    def __setup__(cls):
        super().__setup__()
        cls.prices.states['invisible'] = PYSON_STATEMENT
