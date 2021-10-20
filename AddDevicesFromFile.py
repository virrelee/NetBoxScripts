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
        Field_Order=["InputFileOfSerialNumbers","TypeOfDevice"]

    InputFileOfSerialNumbers = FileVar(
        description="Add the file of Serial Numbers",
        required=True
    
    )
    TypeOfDevice= ObjectVar(
        description = "Choose which Device type you want to add",
        model=DeviceType
    )
    

    def run(self,data,commit):
        ListOfSerialNumbers = data["InputFileOfSerialNumbers"].read().decode("utf-8").strip()
        
        for i in range(len(ListOfSerialNumbers)):     
            Create_Device= Device(
                device_type=data["TypeOfDevice"],
                name="OK",
                site=Site.objects.get(name="Inventory"),
                status= DeviceStatusChoices.STATUS_INVENTORY,
                sevice_Role=DeviceRole.objects.get(name="Unknown"),
                serial= ListOfSerialNumbers[i]
                )

            Create_Device.Save()
            self.log_success(f"Created New Device{Create_Device}")