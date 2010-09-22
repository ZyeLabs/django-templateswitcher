def get_device_family(device):
    max_screen_width = device.get('usableDisplayWidth')
    device_model = device.get('model')
    
    # determine if its an iPad
    if device_model == 'iPad':
        return 'ipad'
    
    # determine screen res
    if max_screen_width <= 240:
        return 'basic'
    else:
        return 'high'
