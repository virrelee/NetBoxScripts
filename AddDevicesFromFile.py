from dcim.choices import DeviceStatusChoices
from dcim.models import Device,DeviceRole,DeviceType,Site
from extras.scripts import *


class Add_Devices(Script):
    class Meta:
        Name= "Add New Devices"
        description= "adding new Devices to Inventory with Status OK"
        Field_Order=["Input File"]

    Input_File = FileVar(
        descripton="Add the file of Serial Numbers",
        required=True
    )
    Number_Of_Devices= IntegerVar(
        description="How many Devices do you wish to Create?"

    )


    def run(self,data,commit):
        for i in range(1,Number_Of_Devices +1):
 
            Create_Device= Device(
                device_type=data,
                Name="OK",
                Site=Site.object.get(Name="Inventory"),
                Status= DeviceStatusChoices.STATUS_INVENTORY,
                Device_Role=DeviceRole.objects.get(Name="Unknown"),
                Serial= Input_File.readlines(i)
                )
            Create_Device.Save()
            self.log_success(f"Created New Device{Create_Device}")