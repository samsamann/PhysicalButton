import flask

from . import button_globals as bg

class PluginApi:
    def __init__(self, plugin):
        self.plugin = plugin

    def get_api_commands(self):
        return dict(
            mock_toogle_pin=['id'],
        )
    
    def on_api_command(self, command, data):
        if command == 'mock_toogle_pin':
            self.plugin.toggleMockPin(int(data.get('id', -1)))

    def on_api_get(self, request):
        return flask.jsonify(dict())
