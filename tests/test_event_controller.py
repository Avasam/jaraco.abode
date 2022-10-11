"""Test the Abode event controller class."""
import json
import unittest
from unittest.mock import call, Mock

import requests_mock

import abodepy
import abodepy.helpers.constants as CONST
import abodepy.helpers.timeline as TIMELINE
from abodepy.devices.binary_sensor import AbodeBinarySensor

import tests.mock.login as LOGIN
import tests.mock.oauth_claims as OAUTH_CLAIMS
import tests.mock.logout as LOGOUT
import tests.mock.panel as PANEL
import tests.mock.devices.secure_barrier as COVER
import tests.mock.devices.door_contact as DOORCONTACT
import tests.mock.devices.ir_camera as IRCAMERA
import pytest


USERNAME = 'foobar'
PASSWORD = 'deadbeef'


class TestEventController(unittest.TestCase):
    """Test the AbodePy event controller."""

    def setUp(self):
        """Set up Abode module."""
        self.abode = abodepy.Abode(
            username=USERNAME, password=PASSWORD, disable_cache=True
        )

    def tearDown(self):
        """Clean up after test."""
        self.abode = None

    @requests_mock.mock()
    def tests_device_id_registration(self, m):
        """Tests that we can register for device events with a device id."""
        # Set up URL's
        m.post(CONST.LOGIN_URL, text=LOGIN.post_response_ok())
        m.get(CONST.OAUTH_TOKEN_URL, text=OAUTH_CLAIMS.get_response_ok())
        m.post(CONST.LOGOUT_URL, text=LOGOUT.post_response_ok())
        m.get(CONST.PANEL_URL, text=PANEL.get_response_ok(mode=CONST.MODE_STANDBY))
        m.get(
            CONST.DEVICES_URL,
            text=COVER.device(
                devid=COVER.DEVICE_ID,
                status=CONST.STATUS_CLOSED,
                low_battery=False,
                no_response=False,
            ),
        )

        # Logout to reset everything
        self.abode.logout()

        # Get our device
        device = self.abode.get_device(COVER.DEVICE_ID)
        assert device is not None

        # Get the event controller
        events = self.abode.events
        assert events is not None

        # Create mock callback
        callback = Mock()

        # Register our device id
        assert events.add_device_callback(device.device_id, callback)

    @requests_mock.mock()
    def tests_device_registration(self, m):
        """Tests that we can register for device events with a device."""
        # Set up URL's
        m.post(CONST.LOGIN_URL, text=LOGIN.post_response_ok())
        m.get(CONST.OAUTH_TOKEN_URL, text=OAUTH_CLAIMS.get_response_ok())
        m.post(CONST.LOGOUT_URL, text=LOGOUT.post_response_ok())
        m.get(CONST.PANEL_URL, text=PANEL.get_response_ok(mode=CONST.MODE_STANDBY))
        m.get(
            CONST.DEVICES_URL,
            text=COVER.device(
                devid=COVER.DEVICE_ID,
                status=CONST.STATUS_CLOSED,
                low_battery=False,
                no_response=False,
            ),
        )

        # Logout to reset everything
        self.abode.logout()

        # Get our device
        device = self.abode.get_device(COVER.DEVICE_ID)
        assert device is not None

        # Get the event controller
        events = self.abode.events
        assert events is not None

        def _our_callback(device):
            assert device is not None

        # Register our device
        assert events.add_device_callback(device, _our_callback)

    @requests_mock.mock()
    def tests_device_all_unregistration(self, m):
        """Tests that we can unregister for all device events."""
        # Set up URL's
        m.post(CONST.LOGIN_URL, text=LOGIN.post_response_ok())
        m.get(CONST.OAUTH_TOKEN_URL, text=OAUTH_CLAIMS.get_response_ok())
        m.post(CONST.LOGOUT_URL, text=LOGOUT.post_response_ok())
        m.get(CONST.PANEL_URL, text=PANEL.get_response_ok(mode=CONST.MODE_STANDBY))
        m.get(
            CONST.DEVICES_URL,
            text=COVER.device(
                devid=COVER.DEVICE_ID,
                status=CONST.STATUS_CLOSED,
                low_battery=False,
                no_response=False,
            ),
        )

        # Logout to reset everything
        self.abode.logout()

        # Get our device
        device = self.abode.get_device(COVER.DEVICE_ID)
        assert device is not None

        # Get the event controller
        events = self.abode.events
        assert events is not None

        def _our_callback(device):
            assert device is not None

        # Register our device
        assert events.add_device_callback(device, _our_callback)

        # Unregister all callbacks
        assert events.remove_all_device_callbacks(device)

    @requests_mock.mock()
    def tests_invalid_device(self, m):
        """Tests that invalid devices are not registered."""
        # Set up URL's
        m.post(CONST.LOGIN_URL, text=LOGIN.post_response_ok())
        m.get(CONST.OAUTH_TOKEN_URL, text=OAUTH_CLAIMS.get_response_ok())
        m.post(CONST.LOGOUT_URL, text=LOGOUT.post_response_ok())
        m.get(CONST.PANEL_URL, text=PANEL.get_response_ok(mode=CONST.MODE_STANDBY))
        m.get(
            CONST.DEVICES_URL,
            text=COVER.device(
                devid=COVER.DEVICE_ID,
                status=CONST.STATUS_CLOSED,
                low_battery=False,
                no_response=False,
            ),
        )

        # Logout to reset everything
        self.abode.logout()

        # Get our device
        device = self.abode.get_device(COVER.DEVICE_ID)
        assert device is not None

        # Get the event controller
        events = self.abode.events
        assert events is not None

        # Create mock callback
        callback = Mock()

        # Test that no device returns false
        assert not events.add_device_callback(None, callback)

        # Create a fake device and attempt to register that
        fake_device = AbodeBinarySensor(json.loads(DOORCONTACT.device()), self.abode)

        with pytest.raises(abodepy.AbodeException):
            events.add_device_callback(fake_device, callback)

    @requests_mock.mock()
    def tests_invalid_all_device_unregister(self, m):
        """Tests that invalid devices are not all unregistered."""
        # Set up URL's
        m.post(CONST.LOGIN_URL, text=LOGIN.post_response_ok())
        m.get(CONST.OAUTH_TOKEN_URL, text=OAUTH_CLAIMS.get_response_ok())
        m.post(CONST.LOGOUT_URL, text=LOGOUT.post_response_ok())
        m.get(CONST.PANEL_URL, text=PANEL.get_response_ok(mode=CONST.MODE_STANDBY))
        m.get(
            CONST.DEVICES_URL,
            text=COVER.device(
                devid=COVER.DEVICE_ID,
                status=CONST.STATUS_CLOSED,
                low_battery=False,
                no_response=False,
            ),
        )

        # Logout to reset everything
        self.abode.logout()

        # Get our device
        device = self.abode.get_device(COVER.DEVICE_ID)
        assert device is not None

        # Get the event controller
        events = self.abode.events
        assert events is not None

        # Test that no device returns false
        assert not events.remove_all_device_callbacks(None)

        # Create a fake device and attempt to unregister that
        fake_device = AbodeBinarySensor(json.loads(DOORCONTACT.device()), self.abode)

        with pytest.raises(abodepy.AbodeException):
            events.remove_all_device_callbacks(fake_device)

    def tests_event_registration(self):
        """Tests that events register correctly."""
        # Get the event controller
        events = self.abode.events
        assert events is not None

        # Create mock callback
        callback = Mock()

        # Test that a valid event registers
        assert events.add_event_callback(TIMELINE.ALARM_GROUP, callback)

        # Test that no event group returns false
        assert not events.add_event_callback(None, callback)

        # Test that an invalid event throws exception
        with pytest.raises(abodepy.AbodeException):
            events.add_event_callback("lol", callback)

    def tests_timeline_registration(self):
        """Tests that timeline events register correctly."""
        # Get the event controller
        events = self.abode.events
        assert events is not None

        # Create mock callback
        callback = Mock()

        # Test that a valid timeline event registers
        assert events.add_timeline_callback(TIMELINE.CAPTURE_IMAGE, callback)

        # Test that no timeline event returns false
        assert not events.add_timeline_callback(None, callback)

        # Test that an invalid timeline event string throws exception
        with pytest.raises(abodepy.AbodeException):
            events.add_timeline_callback("lol", callback)

        # Test that an invalid timeline event dict throws exception
        with pytest.raises(abodepy.AbodeException):
            events.add_timeline_callback({"lol": "lol"}, callback)

    @requests_mock.mock()
    def tests_device_callback(self, m):
        """Tests that device updates callback correctly."""
        # Set up URL's
        m.post(CONST.LOGIN_URL, text=LOGIN.post_response_ok())
        m.get(CONST.OAUTH_TOKEN_URL, text=OAUTH_CLAIMS.get_response_ok())
        m.post(CONST.LOGOUT_URL, text=LOGOUT.post_response_ok())
        m.get(CONST.PANEL_URL, text=PANEL.get_response_ok(mode=CONST.MODE_STANDBY))
        m.get(
            CONST.DEVICES_URL,
            text=COVER.device(
                devid=COVER.DEVICE_ID,
                status=CONST.STATUS_CLOSED,
                low_battery=False,
                no_response=False,
            ),
        )

        # Logout to reset everything
        self.abode.logout()

        # Get our device
        device = self.abode.get_device(COVER.DEVICE_ID)
        assert device is not None

        # Get the event controller
        events = self.abode.events
        assert events is not None

        callback = Mock()

        # Register our device id
        assert events.add_device_callback(device.device_id, callback)

        # Set up device update URL
        device_url = str.replace(CONST.DEVICE_URL, '$DEVID$', COVER.DEVICE_ID)
        m.get(
            device_url,
            text=COVER.device(
                devid=COVER.DEVICE_ID,
                status=CONST.STATUS_OPEN,
                low_battery=False,
                no_response=False,
            ),
        )

        # Call our device callback method
        # pylint: disable=protected-access
        events._on_device_update(device.device_id)
        callback.assert_called_with(device)

        # Test that our device updated
        assert device.status == CONST.STATUS_OPEN

        # Test that no device ID cleanly returns
        events._on_device_update(None)

        # Test that an unknown device cleanly returns
        events._on_device_update(DOORCONTACT.DEVICE_ID)

    def tests_events_callback(self):
        """Tests that event updates callback correctly."""
        # Get the event controller
        events = self.abode.events
        assert events is not None

        # Create mock callbacks
        capture_callback = Mock()
        alarm_callback = Mock()

        # Register our events
        assert events.add_event_callback(TIMELINE.CAPTURE_GROUP, capture_callback)

        assert events.add_event_callback(TIMELINE.ALARM_GROUP, alarm_callback)

        # Call our events callback method and trigger a capture group event
        # pylint: disable=protected-access
        event_json = json.loads(IRCAMERA.timeline_event())
        events._on_timeline_update(event_json)

        # Our capture callback should get one, but our alarm should not
        capture_callback.assert_called_with(event_json)
        alarm_callback.assert_not_called()

        # Test that an invalid event exits cleanly
        events._on_timeline_update({"invalid": "event"})

    def tests_timeline_callback(self):
        """Tests that timeline updates callback correctly."""
        # Get the event controller
        events = self.abode.events
        assert events is not None

        # Create mock callbacks
        all_callback = Mock()
        image_callback = Mock()
        opened_callback = Mock()

        # Register our events
        assert events.add_timeline_callback(TIMELINE.ALL, all_callback)

        assert events.add_timeline_callback(TIMELINE.CAPTURE_IMAGE, image_callback)

        assert events.add_timeline_callback(TIMELINE.OPENED, opened_callback)

        # Call our events callback method and trigger an image capture event
        # pylint: disable=protected-access
        event_json = json.loads(IRCAMERA.timeline_event())
        events._on_timeline_update(event_json)

        # all and image callbacks should have one, opened none
        all_callback.assert_called_with(event_json)
        image_callback.assert_called_with(event_json)
        opened_callback.assert_not_called()

        # Test that an invalid event exits cleanly
        events._on_timeline_update({"invalid": "event"})

    @requests_mock.mock()
    def tests_alarm_callback(self, m):
        """Tests that alarm device updates callback correctly."""
        # Set up URL's
        m.post(CONST.LOGIN_URL, text=LOGIN.post_response_ok())
        m.get(CONST.OAUTH_TOKEN_URL, text=OAUTH_CLAIMS.get_response_ok())
        m.post(CONST.LOGOUT_URL, text=LOGOUT.post_response_ok())
        m.get(CONST.PANEL_URL, text=PANEL.get_response_ok(mode=CONST.MODE_STANDBY))
        m.get(
            CONST.DEVICES_URL,
            text=COVER.device(
                devid=COVER.DEVICE_ID,
                status=CONST.STATUS_CLOSED,
                low_battery=False,
                no_response=False,
            ),
        )

        # Logout to reset everything
        self.abode.logout()

        # Get our alarm device
        alarm = self.abode.get_alarm()
        assert alarm is not None

        # Get the event controller
        events = self.abode.events
        assert events is not None

        callback = Mock()

        # Register our alarm for callback
        assert events.add_device_callback(alarm.device_id, callback)

        # Call our mode changed callback method
        # pylint: disable=protected-access
        events._on_mode_change(CONST.MODE_HOME)
        callback.assert_called_with(alarm)

        # Test that our alarm state is set properly
        assert alarm.mode == CONST.MODE_HOME

        # Test that no mode cleanly returns
        events._on_mode_change(None)

        # Test that an unknown mode cleanly returns
        events._on_mode_change("lol")

    def tests_execute_callback(self):
        """Tests that callbacks that throw exceptions don't bomb."""
        # Get the event controller
        events = self.abode.events
        assert events is not None

        # Create callbacks
        def _callback(event_json):
            raise Exception("CHAOS!!!")

        # Register events callback
        assert events.add_timeline_callback(TIMELINE.CAPTURE_IMAGE, _callback)

        # Call our events callback method and trigger an image capture event
        # pylint: disable=protected-access
        event_json = json.loads(IRCAMERA.timeline_event())
        events._on_timeline_update(event_json)

    @requests_mock.mock()
    def tests_multi_device_callback(self, m):
        """Tests that multiple device updates callback correctly."""
        # Set up URL's
        m.post(CONST.LOGIN_URL, text=LOGIN.post_response_ok())
        m.get(CONST.OAUTH_TOKEN_URL, text=OAUTH_CLAIMS.get_response_ok())
        m.post(CONST.LOGOUT_URL, text=LOGOUT.post_response_ok())
        m.get(CONST.PANEL_URL, text=PANEL.get_response_ok(mode=CONST.MODE_STANDBY))
        m.get(
            CONST.DEVICES_URL,
            text='['
            + COVER.device(
                devid=COVER.DEVICE_ID,
                status=CONST.STATUS_CLOSED,
                low_battery=False,
                no_response=False,
            )
            + ", "
            + DOORCONTACT.device(
                devid=DOORCONTACT.DEVICE_ID, status=CONST.STATUS_CLOSED
            )
            + ']',
        )

        # Logout to reset everything
        self.abode.logout()

        # Get our devices
        cover = self.abode.get_device(COVER.DEVICE_ID)
        assert cover is not None

        doorcontact = self.abode.get_device(DOORCONTACT.DEVICE_ID)
        assert doorcontact is not None

        # Get the event controller
        events = self.abode.events
        assert events is not None

        callback = Mock()

        # Register our devices
        assert events.add_device_callback([cover, doorcontact], callback)

        # Set up device update URL's
        cover_url = str.replace(CONST.DEVICE_URL, '$DEVID$', COVER.DEVICE_ID)
        m.get(
            cover_url,
            text=COVER.device(
                devid=COVER.DEVICE_ID,
                status=CONST.STATUS_OPEN,
                low_battery=False,
                no_response=False,
            ),
        )

        door_url = str.replace(CONST.DEVICE_URL, '$DEVID$', DOORCONTACT.DEVICE_ID)
        m.get(
            door_url,
            text=DOORCONTACT.device(devid=COVER.DEVICE_ID, status=CONST.STATUS_OPEN),
        )

        # Call our device callback method for our cover
        # pylint: disable=protected-access
        events._on_device_update(cover.device_id)
        callback.assert_called_with(cover)

        # Test that our device updated
        assert cover.status == CONST.STATUS_OPEN

        # Test that our other device didn't update
        assert doorcontact.status == CONST.STATUS_CLOSED

        # Call our device callback method for our door contact
        events._on_device_update(doorcontact.device_id)
        callback.assert_has_calls([call(cover), call(doorcontact)])

        # Test that our door updated now
        assert doorcontact.status == CONST.STATUS_OPEN

    def tests_multi_events_callback(self):
        """Tests that multiple event updates callback correctly."""
        # Get the event controller
        events = self.abode.events
        assert events is not None

        # Create mock callback
        callback = Mock()

        # Register our events
        assert events.add_event_callback(
                [TIMELINE.ALARM_GROUP, TIMELINE.CAPTURE_GROUP], callback
            )

        # Call our events callback method and trigger a capture group event
        # pylint: disable=protected-access
        event_json = json.loads(IRCAMERA.timeline_event())
        events._on_timeline_update(event_json)

        # Ensure our callback was called
        callback.assert_called_with(event_json)

    def tests_multi_timeline_callback(self):
        """Tests that multiple timeline updates callback correctly."""
        # Get the event controller
        events = self.abode.events
        assert events is not None

        # Create mock callback
        callback = Mock()

        # Register our events
        assert events.add_timeline_callback(
                [TIMELINE.CAPTURE_IMAGE, TIMELINE.OPENED], callback
            )

        # Call our events callback method and trigger a capture group event
        # pylint: disable=protected-access
        event_json = json.loads(IRCAMERA.timeline_event())
        events._on_timeline_update(event_json)

        # Ensure our callback was called
        callback.assert_called_with(event_json)

    def tests_automations_callback(self):
        """Tests that automation updates callback correctly."""
        # Get the event controller
        events = self.abode.events
        assert events is not None

        # Create mock callbacks
        automation_callback = Mock()

        # Register our events
        assert events.add_event_callback(
                TIMELINE.AUTOMATION_EDIT_GROUP, automation_callback
            )

        # Call our events callback method and trigger a capture group event
        # pylint: disable=protected-access
        events._on_automation_update('{}')

        # Our capture callback should get one, but our alarm should not
        automation_callback.assert_called_with('{}')
