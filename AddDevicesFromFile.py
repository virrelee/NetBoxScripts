## Creator - Viktor Lindgren
## Email - viktor.lindgren@cgi.com
## 

## This Script Will add Devices to Netbox by their Serialnumber and DeviceType
## They will be stored in a site called Inventory 

from dcim.choices import DeviceStatusChoices
from dcim.models import Device,DeviceRole,DeviceType,Site
from extras.scripts import *


class Add_Devices(Script):
    class Meta:
        name= "Add New Devices From File"
        description= "Adding new Devices to Inventory with Status OK"
        Field_Order=["InputFile_Of_SerialNumbers","Type_Of_Device"]

    InputFile_Of_SerialNumbers = FileVar(
        description="Add the file of Serial Numbers",
        required=True
    
    )
    Type_Of_Device= ObjectVar(
        description = "Choose which Device the serial numbers represent",
        model=DeviceType,
        display_field="model"
    )
    

    def run(self,data,commit):
        ListOfSerialNumbers = data["InputFile_Of_SerialNumbers"].read().decode("utf-8").strip()
        
        for i in range(len(ListOfSerialNumbers)):     
            Create_Device= Device(
                device_type=data["Type_Of_Device"],
                name="OK",
                site=Site.objects.get(name="Inventory"),
                status= DeviceStatusChoices.STATUS_INVENTORY,
                service_role=DeviceRole.objects.get(name="Unknown"),
                serial= ListOfSerialNumbers[i]
                )

            Create_Device.Save()
            self.log_success(f"Created New Device{Create_Device}")