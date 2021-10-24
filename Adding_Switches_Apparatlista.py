from numpy import ScalarType
import pandas as pd
#from dcim.models import Device
excel_file = "Apparatlista_SE16.xlsx"
df = pd.read_excel(excel_file, sheet_name="Switchar")
headers = df.columns
#(self,name,device_type,device_role_asset_tag,serial,status,SLA,SLA_Time,ActiDate,IPAddr,Tenant,Region,Site,Level



class model:
    x = "hi"
    # def __init__()
    #     self.name=name
    #     self.device_type=device_type
    #     self.device_role=device_role
    #     self.asset_tag=asste_tag
    #     self.serial=serial
    #     self.status=status
    #     self.SLA=SLA
    #     self.SLA_Time=SLA_Time
    #     self.ActiDate=ActiDate
    #     self.RIR=RIR
    #     self.IPAddr=IPADDR
    #     self.Tenant=Tenant
    #     self.region=region
    #     self.Site=Site
    #     self.Level=Level
    



class Switches(model):
    
    switch = Device(

    )



class DeviceTypes(model):
    
    model = DeviceTypes(

    )



class DeviceRoles(model):
    
    switchRole = DeviceRoles(

    )



class Site(model):

    site = Site()



class Region(model):
    def __init__(regionName):
        self.name=regionName


    region = Region(
        name=self.name
        
    )



class Tenants(model):
    
    tenants = Tentants(

        
    )



class Racks(model):

    racks = Racks(


    )



class IpAdresses(model):
    
    IpAddr = IPAdresses( 


    )

class tags(model):
    tags = Tags(
    )








#(row["name"],row["Hårdvara"],row["Licens typ"],row["SN"],row["SN"],row["status"],row["SLA Nivå"],row["lösningstid"],row["Driftsatt"],row["IPNet"],row["IPAdress"],row["Förvaltning"],row["Ort"],row["Fastighet"])


for index,row in df.itterows():

    region.region(row["Ort"])


