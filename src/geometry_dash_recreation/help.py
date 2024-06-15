"""Modul für das Ausgeben von Hilfetexten."""


def print_help():
    """
    Gibt die Anleitung zur Verwendung des Programms mit den benötigten Parametern in der Kommandozeile aus.

    :return:
    """

    print("\nUSAGE: geometry_dash_recreation <window-width> <window-height> (for windowed mode)")
    print("       geometry_dash_recreation <monitor-nr> (for fullscreen mode)\n")


def print_import():
    """
    Gibt die Nachricht aus, dass geometry_dash_recreation nicht zum Importieren gedacht ist.

    :return:
    """

    print('\nNOTE: geometry_dash_recreation is not meant to be imported and used as a module. '
          'You have to run it with "python3 -m geometry_dash_recreation".\n')
