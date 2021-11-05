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
from extras.models import Tag, TaggedItem
from django.contrib.contenttypes.models import ContentType
from django.utils.text import slugify



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

    Physical_Address = StringVar(
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
                slug=slugify(name),
                region=Region.objects.get(name=data["Region"]),
                facility=row["Krafts anläggning"],
                tenant=Tenant.objects.get(name=data["Tenant"]),
                physical_address=data["Physical_Address"]
            )
            site.save()
            self.log_success(f"Created new Site: {site}")

        def CreateRack(self,row):
            rack = Rack(
                name=row["Ställ"],
                site=Site.objects.get(name=data["Site"]),
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
                device_role=DeviceRole.objects.get(name=row["Licens typ"]),
                #tags=TaggedItem.objects.get(tag="Standard"),
                #manufacturer= Manufacturer.objects.get(name=row["Fabrikat"]),
                device_type=DeviceType.objects.get(model=row["Hårdvara"]),
                serial=row["SN"],
                asset_tag=row["SN"],
                #region=Site.objects.get(name=data["Site"]).region,
                #sitegroup=
                site=Site.objects.get(name=data["Site"]),
                rack=Rack.objects.get(name=row["Ställ"]),
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
                #region=Site.objects.get(name=data["Site"]).region,
                site=Site.objects.get(name=data["Site"]),
                tenant=Site.objects.get(name=data["Site"]).tenant
            )

            prefix.save()
            self.log_success(f"Created new Prefix: {prefix}")

        def CreateIpAddress(self,row):
            assigned_device=Device.objects.get(name=row["Hostname"])
            ipAddress= IPAddress(
                address=row["IPAdress"],
                status=IPAddressStatusChoices.STATUS_ACTIVE,
                tenant=Site.objects.get(name=data["Site"]).tenant,
                #device=Device.objects.get(name=row["Hostname"]),
                assigned_object_type=ContentType.objects.get(model="interface"),
                assigned_object_id=Interface.objects.get(device=assigned_device.id).id

            )
            if not IPAddress.objects.filter(address=row["IPAdress"]).exists():
                ipAddress.save()
                assigned_device.primary_ip4=IPAddress.objects.get(address=row["IPAdress"])
                assigned_device.save()
            else:
                ipa = IPAddress.objects.get(address=row["IPAdress"])
                ipAddress.save()
                assigned_device.primary_ip4=ipAddress
                assigned_device.save()
            self.log_success(f"Created new IPAddress: {ipAddress}")


        excel_file = "/opt/netbox/netbox/scripts/Apparatlista_SE15.xlsx"
        df = pd.read_excel(excel_file, sheet_name="Switchar")
        
        for index,row in df.iterrows():
            if index == 3000:
                break
            if str(data["Site"]) == str(row["Fastighet"]):

                if not Site.objects.filter(name=data["Site"]).exists():
                    CreateSite(self,row)
                if not Rack.objects.filter(name=row["Ställ"]).exists():
                    CreateRack(self,row)
                if not Prefix.objects.filter(prefix=data["Prefix"]).exists():
                    CreatePrefix(self,row)

                if Device.objects.filter(name=row["Hostname"]).exists():
                    if Device.objects.get(name=row["Hostname"]).asset_tag == row["SN"]:
                        continue
                    if Device.objects.get(name=row["Hostname"]).primary_ip4 == row["IPAdress"]:
                        continue

               
                CreateSwitches(self,row)
                CreateInterface(self,row)
                CreateIpAddress(self,row)




               
    

    