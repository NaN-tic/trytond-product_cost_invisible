# This file is part product_cost_invisible module for Tryton.
# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.
from trytond.pool import PoolMeta
from trytond.modules.product_cost_invisible.product import PYSON_STATEMENT


class ShipmentValuedHideMixin(object):
    __slots__ = ()

    @classmethod
    def __setup__(cls):
        super().__setup__()
        cls.currency.states['invisible'] = PYSON_STATEMENT
        cls.untaxed_amount_cache.states['invisible'] = PYSON_STATEMENT
        cls.tax_amount_cache.states['invisible'] = PYSON_STATEMENT
        cls.total_amount_cache.states['invisible'] = PYSON_STATEMENT
        cls.untaxed_amount.states['invisible'] = PYSON_STATEMENT
        cls.tax_amount.states['invisible'] = PYSON_STATEMENT
        cls.total_amount.states['invisible'] = PYSON_STATEMENT


class ShipmentIn(ShipmentValuedHideMixin, metaclass=PoolMeta):
    __name__ = 'stock.shipment.in'


class ShipmentOut(ShipmentValuedHideMixin, metaclass=PoolMeta):
    __name__ = 'stock.shipment.out'


class ShipmentOutReturn(ShipmentValuedHideMixin, metaclass=PoolMeta):
    __name__ = 'stock.shipment.out.return'
