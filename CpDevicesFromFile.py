from django.utils.text import slugify
from dcim.models import Device,DeviceType,DeviceRole,Region,Site
from tenancy.models import Tenant
import pandas as pd
from numpy import nan
from extras.scripts import *
#fuck you
class CpDevicesFromFile(Script):

    class Meta:
        name= "Creating the whole inventory from an new site" #set 25 spaces total
        description= "Copy data from old device to new device and put the old device in Inventory"


    def run(tenantObject,data,commit):
        excel_file = "/opt/netbox/netbox/scripts/Apparatlista_SE16.xlsx"
        df = pd.read_excel(excel_file, sheet_name="Switchar")
        #headers = df.columns
        
        class CreateInventory():
            # def __init__(self,row):
            #     self.Kind_Of_Device_Tag=row[0]
            #     self.DeviceType=row[1]
            #     self.DeviceName=row[2]
            #     self.DeviceStatus=row[3]
            #     self.SLA_tag=row[4]
            #     self.SLA_Time_tag=row[5]
            #     self.ImplementationDate=row[7]
            #     self.RIR=row[8]
            #     self.IPAddr=row[9]
            #     self.Tenant=row[10]
            #     self.Region=row[12]

            def CreateRegion(regionObject):
                
                
                if regionObject.name is nan:
                    return
                if Region.objects.filter(name=regionObject.name).exists():
                    return
                else:
                    region=Region(name=regionObject.name,slug=slugify(regionObject.name))
                    region.save()
                    
                return (tenantObject.Region)
            
            def CreateTenant(tenantObject):
                if tenantObject.name is nan:
                    return
                if Tenant.objects.filter(name=tenantObject.name).exists():
                    return
                else:
                    tenant= Tenant(name=tenantObject.name,slug=slugify(tenantObject.name))
                return (tenantObject.name)


        class CreateRegion():
            def __init__(self,name):
                self.name=name

        class CreateTenant():
            def __init__(self,name):
                self.name=name

        
        
        
        
        RegionList=set()
        TenantList=set()
        for index,row in df.iterrows():
            RegionObject = CreateRegion(row[12])
            TenantObject = CreateTenant(row[10])

            

            RegionOutput = CreateInventory.CreateRegion(RegionObject)
            TenantOutput =  CreateInventory.CreateTenant(TenantObject)
            
            
            if RegionList is None:
                continue
            else:
                RegionList.add(str(RegionOutput))
                TenantList.add(str(TenantOutput))


        Output = f""" Region: {",".join(RegionList)}
                        Tenant: {",".join(TenantList)} 
        """
        return Output





