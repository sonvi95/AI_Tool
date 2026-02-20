from source.module.Control.ModuleSenario import Scenario


class ModuleControler:
    def __init__(self):
        pass

    def get_scenario_database(self,configuration):
        """
        get and save the scenario from the database.
        :param configuration:
        :return:
        """
        senario = Scenario(configuration)
        data_introduce = senario.get_introduce()
        senario.get_question()
        data_ice_phase = senario.get_data_ice_phase()
        print(data_introduce)
        print(data_ice_phase)
        emotion = senario.get_emotion()
        return data_introduce,data_ice_phase,emotion
