from dcim.models import Device,DeviceType,DeviceRole,Region,Site
import pandas as pd
from numpy import nan
#fuck you
class CpDevicesFromFile(Script):

    class Meta:
        name= "Copy Devices From File         " #set 25 spaces total
        description= "Copy data from old device to new device and put the old device in Inventory"
        field_order= ["Start"]

    Start = StringVar(
        name="type something and kick in the script"
    )
    def run(self,data,commit):
        excel_file = "Apparatlista_SE16.xlsx"
        df = pd.read_excel(excel_file, sheet_name="Switchar")
        #headers = df.columns
        set_list=list()
        class CreateInventory():
            def __init__(self,row):
                print (row[12])
                self.Kind_Of_Device_Tag=row[0]
                self.DeviceType=row[1]
                self.DeviceName=row[2]
                self.DeviceStatus=row[3]
                self.SLA_tag=row[4]
                self.SLA_Time_tag=row[5]
                self.ImplementationDate=row[7]
                self.RIR=row[8]
                self.IPAddr=row[9]
                self.Tenant=row[10]
                self.Region=row[12]





            
            def CreateRegion(self):
                
                
                if self.Region is nan:
                    return
                if self.Region in set_list:
                    return
                else:
                    region=Region(name=self.Region)
                    set_list.append(self.Region)
                return (f"Region called {self.Region} has been created")
        output=list()
        for index,row in df.iterrows():
            output.add(CreateInventory(row).CreateRegion())
        return output





