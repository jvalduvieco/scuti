

# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    a_plum_handler = ANicePlumHandler()
    methods = a_plum_handler.handle.methods

    for parameters, result in methods.items():
        print(f"raw effect type: {parameters.types}")
        print(f"effect types: {parameters.effect_types()}")
        print(f"effects are Commands: {parameters.effects_are(Command)}")
        print(f"effects are Event: {parameters.effects_are(Event)}")

        # print(parameters.state_type())

    # print(f"plum took {end - start}")
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
