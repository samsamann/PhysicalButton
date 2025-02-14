from .. import button_globals as bg
from .button_reaction import react_to_input

if bg.debug:
    import gpiozero
    from gpiozero.pins.mock import MockFactory
    gpiozero.Device.pin_factory = MockFactory()

from gpiozero import Button, OutputDevice


def setup_buttons():
    for button in bg.plugin._settings.get(["buttons"]):
        if button.get('gpio') == "none" or not button.get('enabled'):
            continue
        button_gpio = int(button.get('gpio'))
        button_type = button.get('buttonType')
        button_mode = button.get('buttonMode')
        new_button = Button(button_gpio, pull_up=True, bounce_time=None)

        if button_type == 'Toggle':
            bg.plugin._logger.debug(f"Added Buttons: {button_type}")
            new_button.when_pressed = react_to_input
            new_button.when_released = react_to_input
        else:
            if button_mode == "Normally Open (NO)":
                new_button.when_pressed = react_to_input
            if button_mode == "Normally Closed (NC)":
                new_button.when_released = react_to_input
        bg.button_list.append(new_button)
        setup_output_pins(button)
    bg.plugin._logger.debug(f"Added Buttons: {bg.button_list}")
    bg.plugin._logger.debug(f"Added Output devices: {bg.output_list}")


def setup_output_pins(button):
    for activity in list(filter(lambda a: a.get('type') == "output", button.get('activities'))):
        output_gpio = activity.get('execute').get('gpio')
        # check if gpio has to be setup
        if output_gpio == 'none' or int(output_gpio) in list(map(lambda oD: oD.pin.number, bg.output_list)):
            continue
        output_device = OutputDevice(int(output_gpio))
        initial_value = activity.get('execute').get('initial')
        if initial_value == "HIGH":
            output_device.on()
        bg.output_list.append(output_device)


def remove_buttons():
    bg.plugin._logger.debug(f"Buttons to remove: {bg.button_list}")
    for button in bg.button_list:
        button.close()
    bg.button_list.clear()


def remove_outputs():
    bg.plugin._logger.debug(f"Output devices to remove: {bg.output_list}")
    for output_device in bg.output_list:
        output_device.close()
    bg.output_list.clear()
