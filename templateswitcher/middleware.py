import os

from django.conf import settings

from mobile.sniffer.chain import ChainedSniffer

device_families_module = getattr(settings, 'DEVICE_FAMILIES')
device_families = __import__(device_families_module)

class TemplateDirSwitcher(object):
    """
    Template Switching Middleware. Switches template dirs by using preset conditions
    and device families according to the devices capabilities. Returns the device
    object in the request object and resets the TEMPLATE_DIRS attr in the project 
    settings.
    """
    def process_request(self, request):
        if getattr(request, 'device', None):
            template_set = device_families.get_device_family(request.device)
            
            # switch the template dir for the given device
            settings.TEMPLATE_DIRS = (
                settings.DEVICE_TEMPLATE_DIRS[template_set],
            )
        
        else:
            # set the device switcher library according to the settings - defaults to wurfl
            device_switch_libs = getattr(settings, 'DEVICE_SWITCH_LIB', ['WurlfSniffer'])
            da_api = getattr(settings, 'DEVICE_ATLAS_API_FILE', None)
                
            # import requied device library classes
            if 'ApexVertexSniffer' in device_switch_libs:
                from mobile.sniffer.apexvertex.sniffer import ApexVertexSniffer
            if 'WAPProfileSniffer' in device_switch_libs:
                from mobile.sniffer.wapprofile.sniffer import WAPProfileSniffer
            if 'DeviceAtlasSniffer' in device_switch_libs:
                if not os.path.exists(da_api):
                    raise Exception('DEVICE_ATLAS_API_FILE must be in your setting and contain a valid path to use Device Atlas.')
                from mobile.sniffer.deviceatlas.sniffer import DeviceAtlasSniffer
            if 'WurlfSniffer' in device_switch_libs:
                from mobile.sniffer.wurlf.sniffer import WurlfSniffer
            
            chained_libs = []
            for device_lib in device_switch_libs:
                chained_libs.append(eval(device_lib)())
            
            # instantiate the sniffer and device object
            sniffer = ChainedSniffer(chained_libs)
            device_object = sniffer.sniff(request)
            template_set = device_families.get_device_family(device_object)
                
            # copy the device object to the request object
            request.device = device_object
            
            # switch the template dir for the given device
            settings.TEMPLATE_DIRS = (
                settings.DEVICE_TEMPLATE_DIRS[template_set],
            )
