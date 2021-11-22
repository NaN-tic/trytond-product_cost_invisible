# This file is part product_cost_invisible module for Tryton.
# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.
from trytond.pool import PoolMeta, Pool
from trytond.transaction import Transaction
from trytond.pyson import Eval, Id

PYSON_STATEMENT = ~Eval('context', {}).get('groups',
            []).contains(Id('product_cost_invisible', 'group_product_cost_invisible_admin'))


class Template(metaclass=PoolMeta):
    __name__ = 'product.template'

    @classmethod
    def __setup__(cls):
        super().__setup__()
        cls.cost_price.states['invisible'] = PYSON_STATEMENT
        if hasattr(cls, 'cost_value'):
            cls.cost_value.states['invisible'] = PYSON_STATEMENT


class Product(metaclass=PoolMeta):
    __name__ = 'product.product'

    @classmethod
    def __setup__(cls):
        super().__setup__()
        cls.cost_price.states['invisible'] = PYSON_STATEMENT
        cls.cost_price_uom.states['invisible'] = PYSON_STATEMENT
        cls.cost_prices.states['invisible'] = PYSON_STATEMENT
        # stock
        if hasattr(cls, 'cost_value'):
            cls.cost_value.states['invisible'] = PYSON_STATEMENT
        # purchase
        if hasattr(cls, 'purchase_price_uom'):
            cls.purchase_price_uom.states['invisible'] = PYSON_STATEMENT

    @classmethod
    def view_attributes(cls):
        pool = Pool()
        Data = pool.get('ir.model.data')

        is_purchase = False
        is_stock = False
        try:
            Purchase = pool.get('purchase.purchase')
            is_purchase = True
        except KeyError:
            pass
        try:
            Location = pool.get('stock.location')
            is_stock = True
        except KeyError:
            pass

        groups = Transaction().context.get('groups', [])
        product_cost_invisible_admin_group = Data.get_id(
            'product_cost_invisible', 'group_product_cost_invisible_admin')
        not_allowed_user = product_cost_invisible_admin_group not in groups
        view_attributes = [
            ('/tree/field[@name="cost_price_uom"]', 'tree_invisible',
                not_allowed_user),
            ]
        if is_purchase:
            view_attributes +=  [
                ('/tree/field[@name="purchase_price_uom"]', 'tree_invisible',
                    not_allowed_user),
                ('/tree/field[@name="cost_value"]', 'tree_invisible',
                    not_allowed_user),
                ]
        elif is_stock:
            view_attributes +=  [
                ('/tree/field[@name="cost_value"]', 'tree_invisible',
                    not_allowed_user),
                ]
        return super().view_attributes() + view_attributes
