from trytond.pool import PoolMeta, Pool
from trytond.transaction import Transaction
from trytond.modules.product_cost_invisible.product import PYSON_STATEMENT


class Location(metaclass=PoolMeta):
    __name__ = 'stock.location'

    @classmethod
    def __setup__(cls):
        super().__setup__()
        cls.cost_value.states['invisible'] = PYSON_STATEMENT

    @classmethod
    def view_attributes(cls):
        pool = Pool()
        Data = pool.get('ir.model.data')

        groups = Transaction().context.get('groups', [])
        product_cost_invisible_admin_group = Data.get_id(
            'product_cost_invisible', 'group_product_cost_invisible_admin')
        not_allowed_user = product_cost_invisible_admin_group not in groups
        return super().view_attributes() + [
            ('/tree/field[@name="cost_value"]', 'tree_invisible',
                not_allowed_user)]
