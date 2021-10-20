from dcim.choices import DeviceStatusChoices
from dcim.models import Device,DeviceRole,DeviceType,Site
from extras.scripts import *
#commentss

class Add_Devices(Script):
    class Meta:
        name= "Add New Devices From File"
        description= "Adding new Devices to Inventory with Status OK"
        Field_Order=["Input File"]

    InputFileOfSerialNumbers = FileVar(
        description="Add the file of Serial Numbers",
        required=True
    )

    

    def run(self,data,commit):
        ListOfSerialNumbers = data["InputFileOfSerialNumbers"].read().decode("utf-8").strip()
        
        for i in range(len(ListOfSerialNumbers)):     
            Create_Device= Device(
                device_type=data,
                name="OK",
                site=Site.objects.get(name="Inventory"),
                status= DeviceStatusChoices.STATUS_INVENTORY,
                sevice_Role=DeviceRole.objects.get(name="Unknown"),
                serial= ListOfSerialNumbers[i]
                )

            Create_Device.Save()
            self.log_success(f"Created New Device{Create_Device}")