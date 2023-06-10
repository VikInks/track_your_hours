class HoursWork:

    def __init__(self):
        try:
            import json
            import os
            import signal
            from collections import defaultdict

            from improvments.config.config import check_config
            from improvments.handler.signal_handler import signal_handler
            from improvments.utils.menu import main_menu
            from improvments.utils.validation_json_data import validate_and_sort_data
            signal.signal(signal.SIGINT, signal_handler)

            config_file = "config.json"
            data_file = "data.json"
        except ImportError as e:
            raise ImportError(f"Import error: {e}")

        print("Welcome to HoursWork!")
        print("Press Ctrl+C to exit the program.")
        print(config_file)

        def clear_terminal(self):
            os.system('cls' if os.name == 'nt' else 'clear')

        def load_data(self, data_file):
            data = defaultdict(lambda: defaultdict(lambda: defaultdict(dict)))
            if os.path.exists(data_file):
                with open(data_file, 'r') as f:
                    data.update(json.load(f))
                    validate_and_sort_data(data)
            return data

        def load_config(self, config_file):
            config = defaultdict(lambda: defaultdict(lambda: defaultdict(dict)))
            if os.path.exists(config_file):
                with open(config_file, 'r') as f:
                    config.update(json.load(f))
            return config

        check_config(config_file=config_file)
        self.data = load_data(self, data_file=data_file)
        self.config = load_config(self, config_file=config_file)
        while True:
            clear_terminal(self)
            main_menu(self.data, self.config, signal_handler)


if __name__ == '__main__':
    HoursWork()
