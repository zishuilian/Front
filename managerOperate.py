from Core import adminAction


def UpdateBus(obus , nbus ):
    adminAction.adminUpdateBus(obus, nbus)
    return True


def InsertBus(bus):
    adminAction.adminInsertBus(bus)
    return True

