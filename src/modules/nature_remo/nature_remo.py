from remo import NatureRemoAPI


class NatureRemo:

    appliances = None

    def __init__(self, acccess_token: str):
        self.nr_api = NatureRemoAPI(acccess_token)
        self.appliances = self.nr_api.get_appliances()
        self.devices = self.nr_api.get_devices()

    def update_appliances(self):
        """Update the appliances list.
        """
        self.appliances = self.nr_api.get_appliances()

    def search_appliance_by_nickname(
        self,
        nickname: str,
    ):
        """Search the appliance by the nickname.

        Args:
            nickname (str): Nickname of the appliance.

        Returns:
            app (Appliance): Searched appliance object.
        """
        for app in self.appliances:
            if app.nickname == nickname:
                return app

    def get_current_state(
        self,
        target_nickname: str,
    ):
        """Get the current state of the appliance.

        Args:
            target_nickname (str): Nickname of the device.

        Returns:
            current_state (str): Current state of the device.
        """
        self.update_appliances()
        target_device = self.search_appliance_by_nickname(
            target_nickname)

        # FIXME Change the state int the code to match your environment.
        current_state = target_device.light.state.power
        return current_state
