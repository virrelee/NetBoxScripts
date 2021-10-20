from dcim.choices import DeviceStatusChoices
from dcim.models import Device,DeviceRole,DeviceType,Site
from extras.scripts import *
#comment

class Add_Devices(Script):
    class Meta:
        name= "Add New Devices From File"
        description= "Adding new Devices to Inventory with Status OK"
        Field_Order=["Input File"]

    InputFileOfSerialNumbers = FileVar(
        description="Add the file of Serial Numbers",
        required=True
    )

    ListOfSerialNumbers = InputFileOfSerialNumbers.read().encode(encoding="utf-8").strip()

    def run(self,data,commit):

        
        for i in range(len(ListOfSerialNumbers)):     
            Create_Device= Device(
                device_type=data,
                Name="OK",
                Site=Site.object.get(Name="Inventory"),
                Status= DeviceStatusChoices.STATUS_INVENTORY,
                Device_Role=DeviceRole.objects.get(Name="Unknown"),
                Serial= data["ListOfSerialNumbers"][i]
                )

            Create_Device.Save()
            self.log_success(f"Created New Device{Create_Device}")