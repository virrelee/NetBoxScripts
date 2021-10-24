## Creator - Viktor Lindgren
## Email - viktor.lindgren@cgi.com
## 

## This Script Will give a new device an old devices properties and put the old device in
## the inventory.
## to inventoryd
from django.contrib.contenttypes.models import ContentType
from dcim.models import Device,DeviceRole,Site,Interface
from dcim.choices import DeviceStatusChoices
from extras.scripts import *
from ipam.models import IPAddress
from ipam.choices import IPAddressStatusChoices
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
        model=Site,
        query_params= {"name": ["Inventory","Offline"}
    )
    Inventory_Choice= ObjectVar(
        description="Which kind of state do you wish to put the Old Device"
        model=Device,
        query_params: {"Status":["Inventory","Offline"}
    )

    def run(self,data,commit):
        
        oldevice=data["Old_Device"]
        newdevice=Device.objects.get(serial=data["New_Device"])
    #Exctract all data from the old device to the new device    
        newdevice.name=oldevice.name
        newdevice.device_type=oldevice.device_type
        newdevice.device_role=oldevice.device_role
        newdevice.site=oldevice.site
        newdevice.rack=oldevice.rack
        newdevice.primary_ip4=oldevice.primary_ip4
        newdevice.tenant=oldevice.tenant
        newdevice.status=DeviceStatusChoices.STATUS_ACTIVE
        newdeviceinterfaceId = Interface.objects.get(device=newdevice.id).id
        newdeviceIP_ID = Device.objects.filter(name=newdevice).values_list("primary_ip4", flat=True).first()
        ipa = IPAddress.objects.get(id=newdeviceIP_ID)
        ipa.assigned_object_type=ContentType.objects.get(model="interface")
        ipa.assigned_object_id=newdeviceinterfaceId
        ipa.save()
    # Puts the old Device in inventory with right data    
        oldevice.name="OK"
        oldevice.device_role=DeviceRole.objects.get(name="Unknown")
        oldevice.site=Site.objects.get(name=data["Inventory_Choice"])
        oldevice.rack=None
        oldevice.status=DeviceStatusChoices.STATUS_INVENTORY
        oldevice.tenant=None
        oldevice.primary_ip4=None
        oldevice.save()
        #newdevice.name=oldevice.name

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
    