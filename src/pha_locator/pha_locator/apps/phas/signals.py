

def pre_save_pha(sender, instance, **kwargs):
    instance.total_units = instance.low_rent_units + instance.section8_units
    # print "total units:", instance.total_units


def pre_save_city(sender, instance, **kwargs):
    instance.cityStateZip = instance.city + ', ' + instance.state + ' ' + instance.zip
