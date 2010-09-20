def get_device_family(device):
    max_screen_width = device.get('usableDisplayWidth')
    
    # basic device
    if max_screen_width <= 240:
        return 'basic'
    
    # high end device
    if max_screen_width <= 320:
        return 'high'
    
    # ipad and iphone
    if max_screen_width > 320:
        return 'ipad'
