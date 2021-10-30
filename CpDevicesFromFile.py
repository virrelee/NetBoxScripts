
import numpy
from dcim.models import Device,DeviceType,DeviceRole,Region,Site,Rack,Manufacturer
from dcim.choices import SiteStatusChoices, RackStatusChoices
from tenancy.models import Tenant
from django.core.exceptions import ObjectDoesNotExist
import pandas as pd
from random import randint
from numpy import nan,NaN
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
            randslug = str(randint(0,1000))
            slugname+=randslug
            return slugname
        



        class CreateInventory():

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
                elif Tag.objects.filter(name=tagsObject.name).exists():
                    return
                else:
                    tags = Tag(name=tagsObject.name,slug=slugify(tagsObject.name).lower(),description=tagsObject.description)
                    tags.save()
                    self.log_success(f"Created New Tag {tagsObject.name}")
                    return (tagsObject.name)




            def CreateSite(siteObject):
                if siteObject.name is nan:
                    return
                if siteObject.name is None:
                    return
                elif Site.objects.filter(name=siteObject.name).exists():
                    return
                else:
                    try:
                        site=Site(
                            name=siteObject.name,
                            status=SiteStatusChoices.STATUS_ACTIVE,
                            slug=slugify(siteObject.name).lower()

                           
                            )


                        if Region.objects.filter(name=siteObject.region).exists():
                            site.region=Region.objects.get(name=siteObject.region)


                        if Tenant.objects.filter(name=siteObject.tenant).exists():
                            site.tenant=Tenant.objects.get(name=siteObject.tenant)


                        if siteObject.physical_address is not NaN:
                            site.physical_address=siteObject.physical_address


                        if siteObject.facility is not NaN:
                            site.facility=siteObject.facility


                        if siteObject.comments is not NaN:
                            site.comments=siteObject.comments


                        site.save()
                        
#latitude=siteObject.latitude,
#longitude=siteObject.longitude,
                    
                        self.log_success(f"Created New Site {siteObject.name}")
                        return (siteObject.name)
                    except ObjectDoesNotExist as error:
                        pass




                    
            def CreateRack(rackObject):
                if rackObject.name is nan:
                    return

                if rackObject.name is None:
                    return
                else:
                   
                    try:
                        rack=Rack(
                            name=rackObject.name,
                            status=RackStatusChoices.STATUS_ACTIVE,
                        
                            )


                        if Region.objects.filter(name=rackObject.region).exists():
                            rack.region=Region.objects.get(name=rackObject.region)
                            

                        if Tenant.objects.filter(name=rackObject.tenant).exists():
                            rack.tenant=Tenant.objects.get(name=rackObject.tenant)


                        Rack_ID = Site.objects.get(name=rackObject.site).id
                        if Site.objects.filter(name=rackObject.site).exists():
                            if Rack.objects.filter(site=Rack_ID).exists():
                                return
                            else:
                                rack.site=Site.objects.get(name=rackObject.site)


                        if rackObject.facility_id is not NaN:
                            rack.facility_id=rackObject.facility_id


                        if rackObject.facility_id is not NaN:
                            rack.facility_id=rackObject.facility_id


                        if rackObject.comments is not NaN:
                            rack.comments=rackObject.comments
                        rack.save()
                        
                    
                        self.log_success(f"Created New Rack {rackObject.name}")
                        return (rackObject.name)
                    except ObjectDoesNotExist as error:
                        pass
                





            def CreateManufacturers(manufacturersObject):
                if manufacturersObject.name is nan:
                    return

                if manufacturersObject.name is None:
                    return

                elif Manufacturer.objects.filter(name=manufacturersObject.name).exists():
                    return

                else:
                    manufacturers = Manufacturer(
                        name=manufacturersObject.name,
                        slug= slugify(manufacturersObject.name).lower()
                    )

                self.log_success(f"Created Manufacturer {manufacturersObject.name}")
                manufacturers.save()
                return manufacturersObject.name

            def CreateDeviceRole(deviceRoleObject):
                if deviceRoleObject.name is nan:
                    return

                if deviceRoleObject.name is None:
                    return

                elif DeviceRole.objects.filter(name=deviceRoleObject.name).exists():
                    return

                else:
                    devicerole = DeviceRole(
                        name=deviceRoleObject.name,
                        slug= slugify(deviceRoleObject.name).lower()
                    )

                self.log_success(f"Created DeviceRole {deviceRoleObject.name}")
                devicerole.save()
                return deviceRoleObject.name


        class RegionTemplate():
            def __init__(self,name):
                self.name=name

        class TenantTemplate():
            def __init__(self,name):
                self.name=name


        class TagsTemplate():
            def __init__(self,name,description):
                self.name=name
                self.description=description
            
        class CustomFieldsTemplate():
            pass

        class RackTemplate():
            def __init__(self,row):
                self.name=row["Ställ"]
                self.region=row["Ort"]
                self.site=row["Fastighet"]
                self.status=None
                self.facility_id=row["Krafts anläggning"]
                self.tenant=row["Förvaltning"]
                self.comments=[row["Plan"],row["Rum"],row["Anmärkning"]]

        class SiteTemplate():
            def __init__(self,row):
                self.name=row["Fastighet"]
                self.status=None
                self.region=row["Ort"]
                self.facility=row["Krafts anläggning"]
                self.tenant=row["Förvaltning"]
                self.physical_address=row["Adress"]
                self.latitude=row["GPS_LAT"]
                self.longitude=row["GPS_LONG"]
                self.comments=row["Hus"]
        
        class DeviceTypeTemplate():
            def __init__(self,row):
                self.name=row

        class ManufacturersTemplate():
            def __init__(self,row):
                self.name=row
        
        class DeviceRoleTemplate():
            def __init__(self,row):
                self.name=row

        

        RegionList=set()
        TenantList=set()
        TagsList=set()
        SiteList=set()
        RackList=set()
        ManufacturersList=set()
        DeviceRoleList=set()
        df = df.replace(r'^\s*$', "default", regex=True)
        for i in range(3):
        
        

            for index,row in df.iterrows():
                if i == 0:
                    RegionObject = RegionTemplate(row[12])
                    TenantObject = TenantTemplate(row[10])
                    tagsObject = TagsTemplate(row[4],row[5])
                    manufacturersObject= ManufacturersTemplate(row["Fabrikat"])
                    deviceRoleObject = DeviceRoleTemplate(row["Licens Typ"])
                
                    regionOutput = CreateInventory.CreateRegion(RegionObject)
                    tenantOutput =  CreateInventory.CreateTenant(TenantObject)
                    tagsOutput = CreateInventory.CreateTags(tagsObject)
                    manufacturersOutput = CreateInventory.CreateManufacturers(manufacturersObject)
                    deviceRoleOutput = CreateInventory.CreateDeviceRole(deviceRoleObject)
                
                    RegionList.add(str(regionOutput))
                    TenantList.add(str(tenantOutput))
                    TagsList.add(str(tagsOutput))
                    ManufacturersList.add(str(manufacturersOutput))
                    DeviceRoleList.add(str(deviceRoleOutput))
                    
                
                if i == 1:
                    siteObject = SiteTemplate(row)
                    rackObject = RackTemplate(row)

                    SiteOutput = CreateInventory.CreateSite(siteObject)
                    RackOutput = CreateInventory.CreateRack(rackObject)

                    SiteList.add(str(SiteOutput))
                    RackList.add(str(RackOutput))
                
                
                
                
                
                
                
                
                


        RegionList.remove("None")
        TenantList.remove("None")
        TagsList.remove("None")
        SiteList.remove("None")
        RackList.remove("None")
        ManufacturersList.remove("None")
        DeviceRoleList.remove("None")
            


















        Output = f""" 
        Region: {",".join(RegionList)}

        Tenant: {",".join(TenantList)}

        Tags: {",".join(TagsList)}

        Site: {",".join(SiteList)}

        Racks: {",".join(RackList)}

        Manufacturers: {",".join(ManufacturersList)}

        DeviceRole: {",".join(ManufacturersList)}


        """
        return Output





