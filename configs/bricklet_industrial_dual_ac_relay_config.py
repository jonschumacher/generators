# -*- coding: utf-8 -*-

# Redistribution and use in source and binary forms of this file,
# with or without modification, are permitted. See the Creative
# Commons Zero (CC0 1.0) License for more details.

# Industrial Dual AC Relay Bricklet communication config

from generators.configs.openhab_commonconfig import *

com = {
    'author': 'Olaf Lüke <olaf@tinkerforge.com>',
    'api_version': [2, 0, 0],
    'category': 'Bricklet',
    'device_identifier': 2162,
    'name': 'Industrial Dual AC Relay',
    'display_name': 'Industrial Dual AC Relay',
    'manufacturer': 'Tinkerforge',
    'description': {
        'en': 'Two relays to switch AC devices',
        'de': 'Zwei Relais um Wechselstromgeräte zu schalten'
    },
    'released': True,
    'documented': True,
    'discontinued': False,
    'features': [
        'device',
        'comcu_bricklet',
        'bricklet_get_identity'
    ],
    'constant_groups': [],
    'packets': [],
    'examples': []
}

com['constant_groups'].append({
'name': 'Channel LED Config',
'type': 'uint8',
'constants': [('Off', 0),
              ('On', 1),
              ('Show Heartbeat', 2),
              ('Show Channel Status', 3)]
})

com['packets'].append({
'type': 'function',
'name': 'Set Value',
'elements': [('Channel0', 'bool', 1, 'in', {'default': False}),
             ('Channel1', 'bool', 1, 'in', {'default': False})],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Sets the state of the relays, *true* means on and *false* means off.
For example: (true, false) turns relay 0 on and relay 1 off.

If you just want to set one of the relays and don't know the current state
of the other relay, you can get the state with :func:`Get Value` or you
can use :func:`Set Selected Value`.

All running monoflop timers will be aborted if this function is called.
""",
'de':
"""
Setzt den Zustand der Relais, *true* bedeutet ein und *false* aus.
Beispiel: (true, false) schaltet Relais 0 ein und Relais 1 aus.

Wenn nur eines der Relais gesetzt werden soll und der aktuelle Zustand des
anderen Relais nicht bekannt ist, dann kann der Zustand mit :func:`Get Value`
ausgelesen werden oder es kann :func:`Set Selected Value` genutzt werden.

Alle laufenden Monoflop Timer werden abgebrochen, wenn diese Funktion aufgerufen
wird.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Value',
'elements': [('Channel0', 'bool', 1, 'out', {'default': False}),
             ('Channel1', 'bool', 1, 'out', {'default': False})],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Returns the state of the relays, *true* means on and *false* means off.
""",
'de':
"""
Gibt den Zustand der Relais zurück, *true* bedeutet ein und *false* aus.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set Channel LED Config',
'elements': [('Channel', 'uint8', 1, 'in', {'range': (0, 1)}),
             ('Config', 'uint8', 1, 'in', {'constant_group': 'Channel LED Config', 'default': 3})],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Each channel has a corresponding LED. You can turn the LED off, on or show a
heartbeat. You can also set the LED to "Channel Status". In this mode the
LED is on if the channel is high and off otherwise.
""",
'de':
"""
Jeder Kanal hat eine dazugehörige LED. Die LEDs können individuell an- oder
ausgeschaltet werden. Zusätzlich kann ein Heartbeat oder der Kanalstatus
angezeigt werden. Falls Kanalstatus gewählt wird ist die LED an wenn
ein High-Signal am Kanal anliegt und sonst aus.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Channel LED Config',
'elements': [('Channel', 'uint8', 1, 'in', {'range': (0, 1)}),
             ('Config', 'uint8', 1, 'out', {'constant_group': 'Channel LED Config', 'default': 3})],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Returns the channel LED configuration as set by :func:`Set Channel LED Config`
""",
'de':
"""
Gibt die Kanal-LED-Konfiguration zurück, wie von :func:`Set Channel LED Config` gesetzt.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set Monoflop',
'elements': [('Channel', 'uint8', 1, 'in', {'range': (0, 1)}),
             ('Value', 'bool', 1, 'in', {}),
             ('Time', 'uint32', 1, 'in', {'scale': (1, 1000), 'unit': 'Second'})],
'since_firmware': [1, 0, 0],
'doc': ['af', {
'en':
"""
The first parameter can be 0 or 1 (relay 0 or relay 1). The second parameter
is the desired state of the relay (*true* means on and *false* means off).
The third parameter indicates the time that the relay should hold
the state.

If this function is called with the parameters (1, true, 1500):
Relay 1 will turn on and in 1.5s it will turn off again.

A monoflop can be used as a failsafe mechanism. For example: Lets assume you
have a RS485 bus and a Industrial Dual AC Relay Bricklet connected to one of the
slave stacks. You can now call this function every second, with a time parameter
of two seconds. The relay will be on all the time. If now the RS485
connection is lost, the relay will turn off in at most two seconds.
""",
'de':
"""
Der erste Parameter kann 0 oder 1 sein (Relais 0 oder Relais 1). Der zweite
Parameter ist der gewünschte Zustand des Relais (*true* bedeutet ein und
*false* aus). Der dritte Parameter stellt die Zeit dar, welche das
Relais den Zustand halten soll.

Wenn diese Funktion mit den Parametern (1, true, 1500) aufgerufen wird:
Relais 1 wird angeschaltet und nach 1,5s wieder ausgeschaltet.

Ein Monoflop kann als Ausfallsicherung verwendet werden. Beispiel:
Angenommen ein RS485 Bus und ein Industrial Dual AC Relay Bricklet ist an ein Slave
Stapel verbunden. Jetzt kann diese Funktion sekündlich, mit einem Zeitparameter
von 2 Sekunden, aufgerufen werden. Das Relais wird die gesamte Zeit ein sein.
Wenn jetzt die RS485 Verbindung getrennt wird, wird das Relais nach spätestens
zwei Sekunden ausschalten.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Monoflop',
'elements': [('Channel', 'uint8', 1, 'in', {'range': (0, 1)}),
             ('Value', 'bool', 1, 'out', {}),
             ('Time', 'uint32', 1, 'out', {'scale': (1, 1000), 'unit': 'Second'}),
             ('Time Remaining', 'uint32', 1, 'out', {'scale': (1, 1000), 'unit': 'Second'})],
'since_firmware': [1, 0, 0],
'doc': ['af', {
'en':
"""
Returns (for the given relay) the current state and the time as set by
:func:`Set Monoflop` as well as the remaining time until the state flips.

If the timer is not running currently, the remaining time will be returned
as 0.
""",
'de':
"""
Gibt (für das angegebene Relais) den aktuellen Zustand und die Zeit, wie von
:func:`Set Monoflop` gesetzt, sowie die noch verbleibende Zeit bis zum
Zustandswechsel, zurück.

Wenn der Timer aktuell nicht läuft, ist die noch verbleibende Zeit 0.
"""
}]
})

com['packets'].append({
'type': 'callback',
'name': 'Monoflop Done',
'elements': [('Channel', 'uint8', 1, 'out', {'range': (0, 1)}),
             ('Value', 'bool', 1, 'out', {})],
'since_firmware': [1, 0, 0],
'doc': ['c', {
'en':
"""
This callback is triggered whenever a monoflop timer reaches 0. The
parameters contain the relay and the current state of the relay
(the state after the monoflop).
""",
'de':
"""
Dieser Callback wird ausgelöst, wenn ein Monoflop Timer abläuft (0 erreicht).
Die Parameter enthalten das auslösende Relais und den aktuellen
Zustand des Relais (der Zustand nach dem Monoflop).
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set Selected Value',
'elements': [('Channel', 'uint8', 1, 'in', {'range': (0, 1)}),
             ('Value', 'bool', 1, 'in', {})],
'since_firmware': [1, 0, 0],
'doc': ['af', {
'en':
"""
Sets the state of the selected relay, *true* means on and *false*
means off.

A running monoflop timer for the selected relay will be aborted if this function
is called.

The other relay remains untouched.
""",
'de':
"""
Setzt den Zustand des ausgewählten Relais, *true* bedeutet ein und
*false* aus.

Ein laufender Monoflop Timer für das ausgewählte Relais wird abgebrochen, wenn
diese Funktion aufgerufen wird.

Das andere Relais bleibt unverändert.
"""
}]
})

com['examples'].append({
'name': 'Simple',
'functions': [('loop_header', 5, 'Turn relays alternating on/off 10 times with 1 second delay'),
              ('sleep', 1000, None, None),
              ('setter', 'Set Value', [('bool', True), ('bool', False)], None, None),
              ('sleep', 1000, None, None),
              ('setter', 'Set Value', [('bool', False), ('bool', True)], None, None),
              ('loop_footer',)]
})

def relay_channel(channel):
    return {
        'id': 'Relay {}'.format(channel),
        'label': 'Relay {}'.format(channel),
        'description': 'Switches Relay {}. A running monoflop timer for this relay will be aborted if the relay is toggled by this channel.'.format(channel),

        'type': 'Relay',

        'getters': [{
            'packet': 'Get Value',
            'element': 'Channel{}'.format(channel),
            'transform': 'value.channel{} ? OnOffType.ON : OnOffType.OFF'.format(channel)}],

        'callbacks': [{
            'packet': 'Monoflop Done',
            'element': 'Value',
            'filter': 'channel == {}'.format(channel),
            'transform': 'value ? OnOffType.ON : OnOffType.OFF'}],

        'setters': [{
            'packet': 'Set Selected Value',
            'element': 'Value',
            'packet_params': [str(channel), 'cmd == OnOffType.ON'],
            'command_type': "OnOffType"
        }],

    }

def monoflop_channel(channel):
    return {
        'id': 'Monoflop Relay {}'.format(channel),
        'label': 'Monoflop Relay {}'.format(channel),
        'type': 'Monoflop',

        'getters': [{
            'packet': 'Get Monoflop',
            'element': 'Value',
            'packet_params': ['{}'.format(channel)],
            'transform': 'value.value ? OnOffType.ON : OnOffType.OFF'}],

        'setters': [{
            'packet': 'Set Monoflop',
            'packet_params': [str(channel), 'channelCfg.monoflopValue.booleanValue()', 'channelCfg.monoflopDuration'],
            'command_type': "StringType", # Command type has to be string type to be able to use command options.
        }],

        'setter_refreshs': [{
            'channel': 'Relay {}'.format(channel),
            'delay': '0'
        }]
    }

com['openhab'] = {
    'imports': oh_generic_trigger_channel_imports() + ['org.eclipse.smarthome.core.library.types.OnOffType', 'org.eclipse.smarthome.core.library.types.StringType'],
    'param_groups': oh_generic_channel_param_groups(),
    'channels': [relay_channel(i) for i in range(0, 2)] + [monoflop_channel(i) for i in range(0, 2)],
    'channel_types': [
        oh_generic_channel_type('Relay', 'Switch', 'NOT USED', update_style=None, description='NOT USED'),
        {
            'id': 'Monoflop',
            'item_type': 'String',
            'params': [{
                'packet': 'Set Monoflop',
                'element': 'Time',

                'name': 'Monoflop Duration',
                'type': 'integer',
                'default': 1000,
                'unit': 'ms',

                'label': 'Monoflop Duration',
                'description': 'The time that the relay should hold the configured value.',
            },
            {
                'packet': 'Set Monoflop',
                'element': 'Value',

                'name': 'Monoflop Value',
                'type': 'boolean',
                'default': 'true',

                'label': 'Monoflop Value',
                'description': 'The desired value of the specified channel. Activated means relay closed and Deactivated means relay open.',
            }],
            'label': 'NOT USED',
            'description':'Triggers a monoflop as configured',
            'command_options': [('Trigger', 'TRIGGER')]
        }
    ],
    'actions': [{'fn': 'Set Value', 'refreshs': ['Relay 0', 'Relay 1', 'Monoflop Relay 0', 'Monoflop Relay 1']},
                {'fn': 'Set Selected Value', 'refreshs': ['Relay 0', 'Relay 1', 'Monoflop Relay 0', 'Monoflop Relay 1']},
                {'fn': 'Set Monoflop', 'refreshs': ['Relay 0', 'Relay 1', 'Monoflop Relay 0', 'Monoflop Relay 1']},
                'Get Value', 'Get Monoflop']
}
