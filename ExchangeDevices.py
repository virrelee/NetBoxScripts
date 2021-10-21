## Creator - Viktor Lindgren
## Email - viktor.lindgren@cgi.com
## 

## This Script Will give a new device an old devices properties and put the old device in
## the inventory.
## to inventoryd

from dcim.models import Device,DeviceRole,Site,Interface
from dcim.choices import DeviceStatusChoices
from extras.scripts import *

class ExchangeDevices(Script):
    class Meta:
        name= "Exchange Device         " #set 25 spaces total
        description= "Copy data from old device to new device and put the old device in Inventory"
        field_order=["NewDevice","OldDevice"]

    New_Device= StringVar(
        description="Enter Name of the new Device",

    )
    Old_Device= ObjectVar(
        description="Enter name of the device you are going to replace",
        model=Device,
        query_params= {"status": "active"}
    )

    def run(self,data,commit):
        
        oldevice=data["Old_Device"]
        newdevice=Device.objects.get(serial=data["New_Device"])
    #Exctract all data from the old device to the new device    
        oldevicename=oldevice.name
        newdevice.device_type=oldevice.device_type
        newdevice.device_role=oldevice.device_role
        newdevice.site=oldevice.site
        newdevice.rack=oldevice.rack
        newdevice.primary_ip4=oldevice.primary_ip4
        newdevice.tenancy.tenant=oldevice.tenancy.tenant
        newdevice.status=DeviceStatusChoices.STATUS_ACTIVE
    # Puts the old Device in inventory with right data    
        oldevice.name="OK"
        oldevice.device_role=DeviceRole.objects.get(name="Unknown")
        oldevice.site=Site.objects.get(name="Inventory")
        oldevice.rack=None
        oldevice.status=DeviceStatusChoices.STATUS_INVENTORY
        oldevice.tenancy.tenant=None
        oldevice.primary_ip4=None
        oldevice.save()
        newdevice.name=oldevicename
        newdevice.save()
        self.log_success(f"Created New Device {newdevice}")

        output = [
            "Name,DeviceType,DeviceRole,Site,Rack,Status,serial"
        ]
        attrs = [
        newdevice.name,
        newdevice.device_type.model,
        newdevice.device_role.name,
        newdevice.site.name,
        newdevice.rack.name,
        newdevice.status,
        newdevice.serial
        ]
        output.append(",".join(attrs))
        return "\n".join(output)
    