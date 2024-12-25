import properties as ppt
import argparse as ap

from view import main_view


############
#  SCRIPT  #
############

if __name__ == '__main__':
    print("Loading main properties")
    app_name = ppt.get("app_name")
    __version__ = ppt.get("version")

    print()

    print("┏━━━━━━━━━━━━━━━━━━━━━━━━━━━┓")
    print(f"┃ {app_name:^25} ┃")
    print("┗━┯━━━━━━━━━━━━━━━━━━━━━━━┯━┛")
    print(f"  │ Version {__version__:<13} │  ")
    print("  ╰───────────────────────╯  ")
    print()

    parser = ap.ArgumentParser()
    parser.add_argument("-d", "--debug", action="store_true", help="Displays debug information in the HMI")
    parser.add_argument("-nop", "--nopoints", action="store_true", help="Disable point display in order to boost the software performance. Inactive when the --debug option is active.")
    args = parser.parse_args()

    main_view.load(args.debug or not args.nopoints, args.debug)
