from include import *

# npr : number of parallel runs
def main():
    exp = {
        "datasets": ["pumsb.dat", "connect.dat", "chess.dat", "mushroom.dat", "anneal.dat", "heart-cleveland.dat"],
        "suffix": "-closedsky-fat-mincov-3600-closedsky-noclasses-wc.json",
        "timelimit": 3600,
        "npr": 2
    }
    commands = make_commands_exp_mnr(exp)
    launch_exp(commands, exp["npr"])


if __name__ == '__main__':
    main()