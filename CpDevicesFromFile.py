
import numpy
from dcim.models import Device,DeviceType,DeviceRole,Region,Site,Rack,Manufacturer
from dcim.choices import SiteStatusChoices, RackStatusChoices, DeviceStatusChoices
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
        excel_file = "/opt/netbox/netbox/scripts/Apparatlista_SE15.xlsx"
        df = pd.read_excel(excel_file, sheet_name="Switchar")

        def slugify(slugish):
            while True:
                slugname= slugish
                randslug = str(randint(0,100000))
                slugname+=randslug
                if Device.objects.filter(asset_tag=slugname).exists() == False:
                    break
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


            def CreateDeviceType(deviceTypeObject):
                if deviceTypeObject.model is nan:
                    return

                if deviceTypeObject.model is None:
                    return

                elif DeviceType.objects.filter(model=deviceTypeObject.model).exists():
                    return

                else:
                    devicetype = DeviceType(
                        model=deviceTypeObject.model,
                        slug= slugify(deviceTypeObject.model).lower(),
                        manufacturer= Manufacturer.objects.get(name=deviceTypeObject.manufacturer)
                    )

                self.log_success(f"Created DeviceType {deviceTypeObject.model}")
                devicetype.save()
                return deviceTypeObject.model





            def CreateDevice(deviceObject):
                if deviceObject.name is nan or deviceObject.name.upper() is "OK":
                    device = Device(
                        name="OK",
                        device_type=DeviceType.objects.get(model=deviceObject.devicetype),
                        device_role=DeviceRole.objects.get(name="Unknown"),
                        site=Site.objects.get(name="Inventory"),
                        status=DeviceStatusChoices.STATUS_INVENTORY, 
                        
                    )
                    if deviceObject.asset_tag is not nan:
                        device.serial=deviceObject.serial
                        device.asset_tag=deviceObject.serial
                    else:
                        device.asset_tag=slugify(deviceObject.manufacturer).lower()

                    self.log_success(f"Created Device {device.name}")
                    device.save()
                    return device.name
                    

                elif deviceObject.name is None:
                    return


                else:
                    
                    
                    device = Device(
                        name=deviceObject.name)
                        
                    if deviceObject.devicerole is not nan:
                        device.device_role=DeviceRole.objects.get(name=deviceObject.devicerole)
                    else:
                        device.device_role=DeviceRole.objects.get(name="Unknown")

                    if deviceObject.manufacturer is not nan:
                        device.manufacturer=Manufacturer.objects.get(name=deviceObject.manufacturer)

                    if deviceObject.devicetype is not nan:    
                        device.device_type=DeviceType.objects.get(model=deviceObject.devicetype)

                    if deviceObject.serial is not nan:
                        device.serial=deviceObject.serial

                    if deviceObject.asset_tag is not nan:
                        device.asset_tag=deviceObject.serial
                    else:
                        device.asset_tag=slugify(deviceObject.manufacturer).lower()

                    if deviceObject.region is not nan:
                        device.region=Region.objects.get(name=deviceObject.region)

                    if deviceObject.site is not nan:
                        device.site=Site.objects.get(name=deviceObject.site)    
                    else:
                        try:
                            Rack_id = Site.objects.get(name=device.site).id
                            device.site=Rack.objects.filter(name=deviceObject.rack).get(site=Rack_id).site
                        except ObjectDoesNotExist:
                            device.site=Site.objects.get(name="Unknown")

                    
                    if deviceObject.rack is not nan:
                        try:
                            Rack_id = Site.objects.get(name=device.site).id
                            device.rack=Rack.objects.filter(name=deviceObject.rack).get(site=Rack_id)
                        except ObjectDoesNotExist:
                            device.rack=Rack.objects.get(name="Unknown")
                    if deviceObject.status is not nan:
                        device.status=DeviceStatusChoices.STATUS_ACTIVE

                    if deviceObject.tenant is not nan:
                        if Device.objects.filter(name=deviceObject.name).exists():
                            pass
                        else:
                            device.tenant=Tenant.objects.get(name=deviceObject.tenant)

                    #if deviceObject.tags is not nan:
                        #device.tags=Tag.objects.get(name=deviceObject.tags)
                    

                        
                    

                self.log_success(f"Created Device {device.name}")
                device.save()
                return device.name


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
            def __init__(self,row_model,row_manufacturer):
                self.model=row_model
                self.manufacturer=row_manufacturer

        class ManufacturersTemplate():
            def __init__(self,row):
                self.name=row
        
        class DeviceRoleTemplate():
            def __init__(self,row):
                self.name=row

        class DeviceTemplate():
            def __init__(self,row):
                self.name=row["hostname"]
                self.devicerole=row["Licens typ"]
                self.tags=row["SLA Nivå"]
                self.manufacturer=row["Fabrikat"]
                self.devicetype=row["Hårdvara"]
                self.serial=row["SN"]
                self.asset_tag=row["SN"]
                self.region=row["Ort"]
                self.site=row["Fastighet"]
                self.rack=row["Ställ"]
                self.status=None
                self.tenant=row["Förvaltning"]

        RegionList=set()
        TenantList=set()
        TagsList=set()
        SiteList=set()
        RackList=set()
        ManufacturersList=set()
        DeviceRoleList=set()
        DeviceTypeList=set()
        DeviceList=set()
        df = df.replace(r'^\s*$', "default", regex=True)
        for i in range(3):
        
        

            for index,row in df.iterrows():
                if i == 0:
                    RegionObject = RegionTemplate(row[12])
                    TenantObject = TenantTemplate(row[10])
                    tagsObject = TagsTemplate(row[4],row[5])
                    manufacturersObject= ManufacturersTemplate(row["Fabrikat"])
                    deviceRoleObject = DeviceRoleTemplate(row["Licens typ"])
                
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
                    deviceTypeObject = DeviceTypeTemplate(row["Hårdvara"],row["Fabrikat"])

                    SiteOutput = CreateInventory.CreateSite(siteObject)
                    RackOutput = CreateInventory.CreateRack(rackObject)
                    DeviceTypeOutput = CreateInventory.CreateDeviceType(deviceTypeObject)

                    SiteList.add(str(SiteOutput))
                    RackList.add(str(RackOutput))
                    DeviceTypeList.add(str(DeviceTypeOutput))

                if i == 2:
                    deviceObject= DeviceTemplate(row)

                    DeviceOutput = CreateInventory.CreateDevice(deviceObject)

                    DeviceList.add(str(DeviceOutput))

                
                
                
                
                
                
                
                
                


        RegionList.remove("None")
        TenantList.remove("None")
        TagsList.remove("None")
        SiteList.remove("None")
        RackList.remove("None")
        ManufacturersList.remove("None")
        DeviceRoleList.remove("None")
        DeviceTypeList.remove("None")
        DeviceList.remove("None")



















        Output = f""" 
        Region: {",".join(RegionList)}

        Tenant: {",".join(TenantList)}

        Tags: {",".join(TagsList)}

        Site: {",".join(SiteList)}

        Racks: {",".join(RackList)}

        Manufacturers: {",".join(ManufacturersList)}

        DeviceRole: {",".join(DeviceRoleList)}

        DeviceType: {",".join(DeviceTypeList)}

        Devices: {",".join(DeviceList)}


        """
        return Output





