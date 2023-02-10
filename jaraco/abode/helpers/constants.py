# NOTIFICATION CONSTANTS
SOCKETIO_URL = 'wss://my.goabode.com/socket.io/'

SOCKETIO_HEADERS = {
    'Origin': 'https://my.goabode.com/',
}

# DICTIONARIES
MODE_STANDBY = 'standby'
MODE_HOME = 'home'
MODE_AWAY = 'away'

ALL_MODES = [MODE_STANDBY, MODE_HOME, MODE_AWAY]

ALL_MODES_STR = ", ".join(ALL_MODES)

ARMED = dict(home=True, away=True, standby=False)

STATUS_ONLINE = 'Online'
STATUS_OFFLINE = 'Offline'

STATUS_OPEN = 'Open'
STATUS_OPEN_INT = 1
STATUS_CLOSED = 'Closed'
STATUS_CLOSED_INT = 0

STATUS_LOCKOPEN = 'LockOpen'
STATUS_LOCKOPEN_INT = 0
STATUS_LOCKCLOSED = 'LockClosed'
STATUS_LOCKCLOSED_INT = 1

STATUS_ON = 'On'
STATUS_ON_INT = 1
STATUS_OFF = 'Off'
STATUS_OFF_INT = 0

COLOR_MODE_ON = 0
COLOR_MODE_OFF = 2

STATUSES_KEY = 'statuses'
TEMP_STATUS_KEY = 'temperature'
LUX_STATUS_KEY = 'lux'
HUMI_STATUS_KEY = 'humidity'
SENSOR_KEYS = [TEMP_STATUS_KEY, LUX_STATUS_KEY, HUMI_STATUS_KEY]

UNIT_CELSIUS = '°C'
UNIT_FAHRENHEIT = '°F'
UNIT_PERCENT = '%'
UNIT_LUX = 'lx'
LUX = 'lux'

BRIGHTNESS_KEY = 'statusEx'
