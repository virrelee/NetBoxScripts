
from dcim.models import Device,DeviceType,DeviceRole,Region,Site
from tenancy.models import Tenant
import pandas as pd
from random import randint
from numpy import nan
from extras.scripts import *
from extras.models import Tag
#fuck you
class CpDevicesFromFile(Script):

    class Meta:
        name= "Creating the whole inventory from an new site" #set 25 spaces total
        description= "Copy data from old device to new device and put the old device in Inventory"


    def run(self,data,commit):
        excel_file = "/opt/netbox/netbox/scripts/Apparatlista_SE16.xlsx"
        df = pd.read_excel(excel_file, sheet_name="Switchar")

        def slugify(slugish):
            slugname= slugish
            randslug = str(randint(0,100000))
            slugname+=randslug
            return slugname
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
                if regionObject is None:
                    return
                if Region.objects.filter(name=regionObject.name).exists():
                    return
                else:
                    region=Region(name=regionObject.name,slug=slugify(regionObject.name).lower())
                    region.save()
                    self.log_success(f"Created New Region {regionObject.name}")
                    
                    return (regionObject.name)
            
            
            def CreateTenant(tenantObject):
                if tenantObject.name is nan:
                    return
                if tenantObject.name is None:
                    return
                elif Tenant.objects.filter(name=tenantObject.name).exists():
                    return
                else:

                    tenant= Tenant(name=tenantObject.name,slug=slugify(tenantObject.name).lower())
                
                    tenant.save()
                    self.log_success(f"Created New Tenant {tenantObject.name}")
                    return (tenantObject.name)
                    
            
            def CreateTags(tagsObject):
                if tagsObject.name is nan:
                    return
                if tagsObject.name is None:
                    return
                elif Tenant.objects.filter(name=tagsObject.name).exists():
                    return
                else:
                    tags = Tag(name=tagsObject.name,slug=slugify(tagsObject.name).lower(),description=tagsObject.description)
                    tags.save()
                    self.log_success(f"Created New Tag {tagsObject.name}")
                    return (tagsObject.name)
                    


            
        class RegionTemplate():
            def __init__(self,name):
                self.name=name

        class TenantTemplate():
            def __init__(self,name):
                self.name=name


        class TagsTemplate():
            def __init__(name,description):
                self.name=name
                self.description=description
            


        class SiteTemplate():
            def __init__(self,name,status,region,facility,tenant,physical_address,latitude,longitude,comments):
                self.name=name
                self.status=status
                self.region=region
                self.facility=facility
                self.tenant=tenant
                self.physical_address=physical_address
                self.latitude=latitude
                self.longitude=longitude
                self.comments=comments


        
 
        
        
        RegionList=set()
        TenantList=set()
        TagsList=set()
        for index,row in df.iterrows():
            RegionObject = RegionTemplate(row[12])
            TenantObject = TenantTemplate(row[10])
            tagsObject = TagsTemplate(row[4],row[5])


            

            RegionOutput = CreateInventory.CreateRegion(RegionObject)
            TenantOutput =  CreateInventory.CreateTenant(TenantObject)
            TagsOutput = CreateInventory.CreateTags(tagsObject)
              
            RegionList.add(str(RegionOutput))
            TenantList.add(str(TenantOutput))
            TagsList.add(str(TagsOutput))

        RegionList.remove("None")
        TenantList.remove("None")
        TagsList.remove("None")
            
              

        Output = f""" 
        Region: {",".join(RegionList)}


        Tenant: {",".join(TenantList)}

        Tags: {",".join(TenantList)}
        """
        return Output





