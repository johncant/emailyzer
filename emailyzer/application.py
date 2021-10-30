from emailyzer.scaffold import NotmuchDefaultDatabase


def test_objects():
    # Hardcoded defaults for testing

    return [NotmuchDefaultDatabase()]


class Application:

    def name(self):
        "Emailyzer"

    def display_objects(self):
        return test_objects()
