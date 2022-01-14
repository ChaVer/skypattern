from include import *

# npr : number of parallel runs
def main():
    exp = {
        "datasets": ["pumsb.dat", "connect.dat", "chess.dat", "mushroom.dat", "anneal.dat", "heart-cleveland.dat"],
        "subcommands": [closedsky, closedsky, cpsky],
        "wc": [False, True, False],
        "measures": measures_exp_c,
        "timelimit": 3600,
        "npr": 2,
        "patterntype": "closedsky",
        "strategy": "mincov",
        "noclasses": False
    }
    commands = make_commands_exp_sky(exp)
    # exp 2 : {freq, area, aconf}
    exp["measures"] = [[freq_area_aconf]]
    exp["savepatterns"] = True
    exp["noclasses"] = True
    exp["cst"] = ["lmin=2"]
    commands += make_commands_exp_sky(exp)
    launch_exp(commands, exp["npr"])


if __name__ == '__main__':
    main()
