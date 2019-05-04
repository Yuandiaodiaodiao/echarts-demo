
from datasetOrm import Food


def prn_obj(obj):
    print('\n'.join(['%s:%s' % item for item in obj.__dict__.items()]))


for index, item in enumerate(Food.select()):
    if index > 10: break
    prn_obj(item)
