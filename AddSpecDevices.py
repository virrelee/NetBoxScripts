import numpy
from dcim.models import Device,DeviceType,DeviceRole,Region,Site,Rack,Manufacturer,Interface
from dcim.choices import SiteStatusChoices, RackStatusChoices, DeviceStatusChoices, InterfaceTypeChoices, InterfaceModeChoices
from tenancy.models import Tenant
from ipam.models import Prefix,IPAddress
from ipam.choices import PrefixStatusChoices, IPAddressStatusChoices
from django.core.exceptions import ObjectDoesNotExist
import pandas as pd
from numpy import nan,NaN
from extras.scripts import *
from extras.models import Tag
from django.contrib.contenttypes.models import ContentType



class InventoryFromSite(Script):
    class Meta:
        name= "Inventory From Site" #set 25 spaces total
        description= "Creating Inventory by having the Site as a Backbone"
        field_order=["SiteName","Region","Tenant","Physical_Adress","Prefix"]

    # Variables That has to be put in

    Site = StringVar(
        description="New Site",
        required=True
    )

    Region = ObjectVar(
        description = "Choose Region",
        model=Region,
        required=True        

    )

    Tenant = ObjectVar(
        description= "Choose Tenant",
        model=Tenant,
        required=True
    )

    Physical_Adress = StringVar(
        description="Address for the Site",
        required=True
    )


    Prefix = StringVar(
        description="Enter prefix for the site"
    )

    
    def run(self,data,commit):
    

        def CreateSite(self,row):
            site = Site(
                name=data["Site"],
                region=Region.objects.get(name=data["Region"]),
                facility=row["Krafts Anläggning"],
                tenant=Tenant.objects.get(name=data["Tenant"]),
                physical_address=data["Physical Address"]
            )
            site.save()
            self.log_success(f"Created new Site: {site}")

        def CreateRack(self,row):
            rack = Rack(
                name=row["Ställ"],
                region=Region.objects.get(name=data["Region"]),
                facility_id=row["Krafts Anläggning"],
                tenant=Tenant.objects.get(name=data["Tenant"]),
                status=RackStatusChoices.STATUS_ACTIVE,
                asset_tag=f"{row['Ställ']}-{data['Site']}",
                comments=row["Rum"]
            )
            rack.save()
            self.log_success(f"Created new Rack: {rack}")

        def CreateSwitches(self,row):
            device = Device(
                name=row["Hostname"],
                device_role=DeviceRole.objects.get(name=row["Licens Typ"]),
                tags=[Tag.objects.get(name=row["Typ"]),Tag.objects.get(name=row["SLA Nivå"])],
                manufacturer= Manufacturer.objects.get(name=row["Fabrikat"]),
                device_type=DeviceType.objects.get(model=row["Hårdvara"]),
                serial=row["SN"],
                asset_tag=row["SN"],
                region=Site.objects.get(site=data["Site"]).region,
                #sitegroup=
                site=Site.objects.get(site=data["Site"]),
                rack=Rack.Objects.get(name=row["Ställ"]),
                status=DeviceStatusChoices.STATUS_ACTIVE,
                tenant=Site.objects.get(name=data["Site"]).tenant

            )
            device.save()
            self.log_success(f"Created new Switch: {device}")
        

        def CreateInterface(self,row):
            interface= Interface(
                device=Device.objects.get(name=row["Hostname"]),
                name="MGMT",
                type=InterfaceTypeChoices.TYPE_VIRTUAL,
                #mac=row["MAC"],
                mode=InterfaceModeChoices.MODE_TAGGED,


            )
            interface.save()
            self.log_success(f"Created new Interface: {interface}")

        def CreatePrefix(self,row):
            prefix = Prefix(
                prefix=data["Prefix"],
                status=PrefixStatusChoices.STATUS_ACTIVE,
                region=Site.objects.get(site=data["Site"]).region,
                site=Site.objects.get(site=data["Site"]),
                tenant=Site.objects.get(site=data["Site"]).tenant
            )

            prefix.save()
            self.log_success(f"Created new Prefix: {prefix}")

        def CreateIpAddress(self,row):
            assigned_device=Device.objects.get(name=row["Hostname"])
            ipAddress= IPAddress(
                address=row["IPAdress"],
                status=IPAddressStatusChoices.STATUS_ACTIVE,
                tenant=Site.objects.get(site=data["Site"]).tenant,
                device=Device.objects.get(name=row["Hostname"]),
                assigned_object_type=ContentType.objects.get(model="interface"),
                assigned_object_id=Interface.objects.get(device=assigned_device.id).id

            )
            ipAddress.save()
            self.log_success(f"Created new IPAddress: {ipAddress}")
        
        excel_file = "/opt/netbox/netbox/scripts/Apparatlista_SE15.xlsx"
        df = pd.read_excel(excel_file, sheet_name="Accesspunkter")
        
        for index,row in df.iterrows():
            if "Sara Kulturhus" in str(row["Fastighet"]):
                CreateSite(self,row)
                CreateRack(self,row)
                CreateSwitches(self,row)
                CreateInterface(self,row)
                CreatePrefix(self,row)
                CreateIpAddress(self,row)
    

    