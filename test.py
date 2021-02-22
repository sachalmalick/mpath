import utils.admin_utils as adu
import utils.db_utils as dbu

dbu.create_tables()
adu.run_tests()
print(dbu.get_all_accounts())
