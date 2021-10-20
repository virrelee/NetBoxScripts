from dcim.models import Device,DeviceType,DeviceRole,Site
from dcim.choices import DeviceStatusChoices
from extras.scripts import *
class ExchangeDevice(Script):
    class metadata:
        name= "Exchange Device"
        description="Copy Data From old Device to New Device and puts the old device in inventory"
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
        
        oldevice=data["Old_Device"]
        newdevice=data["NewDevice"]
    #Exctract all data from the old device to the new device    
        oldevicename=oldevice.name
        newdevice.device_type=oldevice.device_type
        newdevice.device_role=oldevice.device_role
        newdevice.site=oldevice.site
        newdevice.rack=oldevice.rack
        newdevice.status=DeviceStatusChoices.STATUS_ACTIVE
    # Puts the old Device in inventory with right data    
        oldevice.name="OK"
        oldevice.device_role=DeviceRole.objects.get(name="Unknown")
        oldevice.site=Site.objects.get(name="Inventory")
        oldevice.rack=None
        oldevice.status=DeviceStatusChoices.STATUS_INVENTORY
        oldevice.save()
        newdevice.name=oldevicename
        newdevice.save()
        self.log_success(f"Created New Device {newdevice}")

        #output = [
        #    "Name,DeviceType,DeviceRole,Site,Rack,Status"
        #]
        #for devices in Device.objects.