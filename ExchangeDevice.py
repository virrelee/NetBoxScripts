from dcim.models import Device,DeviceType,DeviceRole,Site
from dcim.choices import DeviceStatusChoices
from extras.scripts import *
class ExchangeDevice(Script):
    class metadata:
        name="Exchange Device"
        description="Copy Data From old Device to New Device"
        field_order=["NewDevice","OldDevice"]

    NewDevice= ObjectVar(
        description="Enter Name of the new Device",
        model=Device

    )
    Old_Device= ObjectVar(
        description="Enter name of the device you are going to replace",
        model=Device
    )

    def run(self,data,commit):
        #oldevice= Device.objects.get(name=data["Old_Device"])
        #newdevice= Device.objects.get(name=data["NewDevice"]
        oldevice=data["Old_Device"]
        newdevice=data["NewDevice"]
        oldevicename=oldevice.name
        newdevice.device_type=oldevice.device_type
        newdevice.device_role=oldevice.device_role
        newdevice.site=oldevice.site
        newdevice.rack=oldevice.rack
        newdevice.status=DeviceStatusChoices.STATUS_ACTIVE
        oldevice.name="OK"
        oldevice.device_role=DeviceRole.objects.get(name="Unknown")
        oldevice.site=Site.objects.get(name="Inventory")
        oldevice.rack=None
        oldevice.status=DeviceStatusChoices.STATUS_INVENTORY
        oldevice.save()
        newdevice.name=oldevicename
        newdevice.save()
        self.log_success(f"Created New Device {newdevice}")