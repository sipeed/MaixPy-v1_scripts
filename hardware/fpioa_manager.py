from Maix import FPIOA

class fm:
  fpioa = FPIOA()

  def help():
    __class__.fpioa.help()

  def get_pin_by_function(function):
    return __class__.fpioa.get_Pin_num(function)

  def register(pin, function, force=False):
    pin_used = __class__.get_pin_by_function(function)
    if pin_used == pin:
      return 
    if None != pin_used:
      info = "[Warning] function is used by %s(pin:%d)" % (
          fm.str_function(function), pin_used)
      if force == False:
        raise Exception(info)
      else:
        print(info)
    __class__.fpioa.set_function(pin, function)

  def unregister(pin):
    __class__.fpioa.set_function(pin, fm.fpioa.RESV0)

  def str_function(function):
    if fm.fpioa.GPIOHS0 <= function and function <= fm.fpioa.GPIO7:
      if fm.fpioa.GPIO0 <= function:
        return 'fm.fpioa.GPIO%d' % (function - fm.fpioa.GPIO0)
      return 'fm.fpioa.GPIOHS%d' % (function - fm.fpioa.GPIOHS0)
    return 'unknown'

  def get_gpio_used():
    return [(__class__.str_function(f), __class__.get_pin_by_function(f)) for f in range(fm.fpioa.GPIOHS0, fm.fpioa.GPIO7 + 1)]


if __name__ == "__main__":
  import time
  print('check register')
  for item in fm.get_gpio_used():
    print(item)
  print('test unregister')
  for pin in range(8, 48):
    fm.unregister(pin)
  print('check register')
  for item in fm.get_gpio_used():
    print(item)
  # gpio test
  from Maix import GPIO

  def gpio_test():
    for i in range(5):
      led_b.value(1)
      led_g.value(1)
      time.sleep_ms(100)
      print('woking...')
      led_b.value(0)
      led_g.value(0)
      time.sleep_ms(100)
      print('woking...')
  print('register...')
  fm.register(12, fm.fpioa.GPIO0)
  fm.register(13, fm.fpioa.GPIOHS0)
  led_b = GPIO(GPIO.GPIO0, GPIO.OUT)
  led_g = GPIO(GPIO.GPIOHS0, GPIO.OUT)
  gpio_test()
  print('unregister...')
  fm.unregister(12)
  fm.unregister(13)
  gpio_test()
  print('register...')
  fm.register(12, fm.fpioa.GPIO0)
  fm.register(13, fm.fpioa.GPIOHS0)
  gpio_test()
  fm.unregister(12)
  fm.unregister(13)
  # register Coverage test
  fm.register(12, fm.fpioa.GPIO0)
  time.sleep_ms(500)
  try:
    fm.register(13, fm.fpioa.GPIO0)  # fail
  except Exception as e:
    print('Exception')
    print(e)
  time.sleep_ms(500)
  fm.register(12, fm.fpioa.GPIOHS0)  # pass
  time.sleep_ms(500)
  print('Warning')
  fm.register(13, fm.fpioa.GPIOHS0, force=True)  # pass
  time.sleep_ms(500)
  fm.unregister(12)
  fm.unregister(13)
