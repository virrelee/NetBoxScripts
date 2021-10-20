## Creator - Viktor Lindgren
## Email - viktor.lindgren@cgi.com
## 

## This Script Will add Devices to Netbox by their Serialnumber and DeviceType
## They will be stored in a site called Inventory 

from typing import List
from dcim.choices import DeviceStatusChoices
from dcim.models import Device,DeviceRole,DeviceType,Site
from extras.scripts import *


class Add_Devices(Script):
    class Meta:
        name= "Add New Devices From File"
        description= "Adding new Devices to Inventory with Status OK"
        field_Order=["InputFile_Of_SerialNumbers","Type_Of_Device"]

    File_With_SerialNumbers = FileVar(
        description="Add the file that contains all Serial Numbers (.txt,.csv)",
        required=True
    
    )
    Type_Of_Device= ObjectVar(
        description = "Choose which DeviceType the serial numbers represent",
        model=DeviceType,
        display_field="model"
    )
    

    def run(self,data,commit):
        ListOfSerialNumbers = data["File_With_SerialNumbers"].read().decode("utf-8").split()
        
        for i in range(len(ListOfSerialNumbers)):     
            Create_Device= Device(
                device_type=data["Type_Of_Device"],
                name="OK",
                site=Site.objects.get(name="Inventory"),
                status= DeviceStatusChoices.STATUS_INVENTORY,
                device_role=DeviceRole.objects.get(name="Unknown"),
                #asset_tag= ListOfSerialNumbers[i],
                serial= ListOfSerialNumbers[i]
                )

            Create_Device.save()
            self.log_success(f"Created New Device with serial-Number {ListOfSerialNumbers[i]}")
        
#Create a CSV-File
        output = [
            "Name,Serial Number,Device Type,Device Role,Status"
        ]
        for Devices in Device.objects.filter(site=Create_Device.site):
            attrs =  [
                Devices.name,
                Devices.serial,
                Devices.device_type.model,
                Devices.device_role.name,
                Devices.status
        ]   
            output.append(",".join(attrs))

        return "\n".join(output)
