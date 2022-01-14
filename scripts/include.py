import os
import subprocess
import operator as op
import json
import re
import time
from concurrent import futures
from functools import reduce
from pathlib import Path
from parse_patterns import parse_json_patterns


# some basic function
def is_int(n):
    try:
        float_n = float(n)
        int_n = int(float_n)
    except ValueError:
        return False
    else:
        return float_n == int_n


def is_float(n):
    try:
        float_n = float(n)
    except ValueError:
        return False
    else:
        return True


def ncr(n, r):
    r = min(r, n - r)
    numer = reduce(op.mul, range(n, n - r, -1), 1)
    denom = reduce(op.mul, range(1, r + 1), 1)
    return numer / denom


# Print iterations progress
def printProgressBar(iteration, total, prefix='', suffix='', decimals=1, length=100, fill='█', printEnd="\r"):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
        printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print('\r%s |%s| %s%% %s' % (prefix, bar, percent, suffix), end=printEnd)
    # Print New Line on Complete
    if iteration == total:
        print()


# set the root directory
cwd = os.path.dirname(os.path.realpath(__file__))
project_dir = os.path.abspath(os.path.join(cwd, os.pardir))

# preparing  project directories directories
project_data_dir = os.path.abspath(os.path.join(project_dir, "data"))
project_res_dir = os.path.abspath(os.path.join(project_dir, "results"))
project_conf_dir = os.path.abspath(os.path.join(project_dir, "conf"))
project_log_file = os.path.abspath(os.path.join(project_dir, "logs", "logs.txt"))
project_scripts_dir = os.path.abspath(os.path.join(project_dir, "scripts"))

java_path = "/usr/lib/jvm/java-11-openjdk-amd64/bin/java"
project_jar = os.path.abspath(os.path.join(project_dir, "target", "skypattern-1-jar-with-dependencies.jar"))


# Datasets
chess = "chess.dat"
hepatitis = "hepatitis.dat"
kr_vs_kp = "kr-vs-kp.dat"
connect = "connect.dat"
heart_cleveland = "heart-cleveland.dat"
splice1 = "splice1.dat"
mushroom = "mushroom.dat"
t40 = "T40I10D100K.dat"
pumsb = "pumsb.dat"
t10 = "T10I4D100K.dat"
bms1 = "BMS1.dat"
retail = "retail.dat"
iris = "iris.dat"
zoo = "zoo.dat"

# Measures
# Pattern measures
freq_area_gr = "fag"
freq_area_aconf = "fat"
freq_area = "fa"
freq_gr = "fg"
area_gr = "ag"
freq = "f"
area = "a"
# Attribute measures
mean_max_min_val = "nMm"
mean_max_val = "nM"
min_max_val = "mM"
mean_min_val = "nm"
mean_val = "n"
max_val = "M"
min_val = "m"


measures_exp_c = [
    [freq_area_gr, mean_val],
    [freq_area_gr, max_val],
    [freq_area, mean_max_val],
    [freq_gr, mean_max_val],
    [area_gr, mean_max_val],
    [freq_area_gr, mean_max_val]
]

measures_exp_c2 = [
    [freq_area_gr],
    [freq_area],
    [freq_gr],
    [area_gr]
]

measures_exp_c3 = [
    [freq_area, min_max_val],
    [freq_area, mean_min_val],
    [area_gr, min_max_val],
    [area_gr, mean_min_val],
    [freq_gr, min_max_val],
    [freq_gr, mean_min_val]
]

measures_exp_c4 = [
    [freq_area_gr, min_max_val],
    [freq_area_gr, mean_min_val],
    [freq_area_gr, mean_max_min_val]
]

measures_exp_nc = [
    [freq_area],
    [freq_area, max_val],
    [freq_area, mean_val],
    [freq, mean_max_val],
    [area, mean_max_val]
]

measures_exp_nc2 = [
    [freq_area, min_val],
    [freq_area, mean_min_val],
    [freq_area, mean_max_val],
    [freq_area, mean_max_min_val]
]

measures_splice1 = [
    [freq_area],
    [freq_gr],
    [freq_area, min_max_val],
    [freq_area, mean_min_val],
    [freq_gr, min_max_val]
]

measures_connect = [
    [area_gr],
    [freq_area],
    [freq_gr],
    [freq_area_gr],
    [area_gr, min_max_val],
    [freq_area, min_max_val],
    [freq_area, mean_min_val],
    [freq_gr, min_max_val],
    [freq_gr, mean_min_val],
    [freq_area_gr, min_max_val]
]

measures_pumsb = [
    [freq_area],
    [freq_area, min_max_val],
    [freq_area, mean_min_val]
]

# Commands
cpsky = "cpsky"
closedsky = "closedsky"

noclasses = "noclasses"
threshold = "threshold"

dataset_infos = {
    chess: {
        noclasses: False,
        threshold: [0.3, 0.2, 0.1]
    },
    hepatitis: {
        noclasses: False,
        threshold: [0.2, 0.1, 0.05]
    },
    kr_vs_kp: {
        noclasses: False,
        threshold: [0.3, 0.2]
    },
    connect: {
        noclasses: False,
        threshold: [0.18, 0.15, 0.1]
    },
    heart_cleveland: {
        noclasses: False,
        threshold: [0.1, 0.08, 0.06]
    },
    splice1: {
        noclasses: False,
        threshold: [0.1, 0.05, 0.02]
    },
    mushroom: {
        noclasses: False,
        threshold: [0.01, 0.008, 0.005]
    },
    t40: {
        noclasses: True,
        threshold: [0.08, 0.05, 0.01]
    },
    pumsb: {
        noclasses: False,
        threshold: [0.8, 0.7]
    },
    t10: {
        noclasses: True,
        threshold: [0.005, 0.0025]
    },
    bms1: {
        noclasses: True,
        threshold: [0.001, 0.0005]
    },
    retail: {
        noclasses: True,
        threshold: [0.004, 0.002]
    },
    iris: {
        noclasses: False,
        threshold: [0.02, 0.01]
    },
    zoo: {
        noclasses: False,
        threshold: [0.02, 0.01]
    }
}

dataset_classes = [chess, hepatitis, kr_vs_kp, connect, heart_cleveland, splice1, mushroom, pumsb]
dataset_classes_wc = [connect, splice1, pumsb]
dataset_classes_dc = [chess, hepatitis, kr_vs_kp, heart_cleveland, mushroom]
dataset_noclasses = [t40, t10, bms1, retail]
dataset_test = [zoo, iris]
dataset_todo = [bms1, chess, mushroom, pumsb]


def convert_datasets_name_aetheris(datasets):
    return [os.path.splitext(dataset)[0] + ".aet" for dataset in datasets]


def make_command(config):
    classes = "noclasses" if config["noclasses"] else "classes"
    res_json = project_res_dir + "/" + Path(config["data"]).stem + "-" + config["subcommand"] + "-" + config[
        "pmeasures"]
    command = [java_path, "-jar", project_jar, config["subcommand"], "-d", config["data"], "--dat", "-m",
               config["pmeasures"]]
    if config["ameasures"] != "":
        res_json += config["ameasures"]
        command += ["-v", config["ameasures"]]
    res_json += "-" + config["strategy"] + "-" + config["timelimit"] + "-" + config["patterntype"] + "-" + classes
    if config["noclasses"]:
        command += ["--nc"]
    if "savepatterns" in config:
        command += ["--sp"]
    if "theta" in config:
        theta = str(config["theta"])
        command += ["--cst", "rfmin=" + theta]
        res_json += "-" + theta
    if "wc" in config and config["subcommand"] == closedsky:
        command += ["--wc"]
        res_json += "-wc"
    if "cst" in config:
        for c in config["cst"]:
            command += ["--cst", c]
    res_json += ".json"
    command += ["--str", config["strategy"], "--tl", config["timelimit"], "--json", res_json, "--pt",
                config["patterntype"]]
    return command


def make_configs(exp):
    configs = []
    for dataset in exp["datasets"]:
        for m in exp["measures"]:
            for subcommand in exp["subcommands"]:
                config = {
                    "data": os.path.join(project_data_dir, dataset),
                    "subcommand": subcommand,
                    "pmeasures": m[0],
                    "ameasures": m[1] if len(m) > 1 else "",
                    "strategy": exp["strategy"],
                    "timelimit": exp["timelimit"],
                    "patterntype": exp["patterntype"],
                    "noclasses": dataset_infos[dataset][noclasses] if "noclasses" not in exp else exp["noclasses"],
                    "cst": exp["cst"]
                }
                if "wc" in exp:
                    config["wc"] = True
                if "savepatterns" in exp:
                    config["savepatterns"] = True
                if threshold in exp:
                    for t in dataset_infos[dataset][threshold]:
                        config["theta"] = t
                        configs.append(config.copy())
                else:
                    configs.append(config)
    return configs


def launch_command(command):
    print("Start " + " ".join(command))
    subprocess.run(command)
    print("End " + " ".join(command))
    return command


def launch_experiment(exp, exp_name):
    commands = [make_command(config) for config in make_configs(exp)]
    executor = futures.ThreadPoolExecutor(max_workers=exp["npr"])
    res = [executor.submit(launch_command, command) for command in commands]
    iteration = 0
    log_file = open(project_log_file, 'a')
    log_file.write("Start experiment " + exp_name + "\n")
    for f in futures.as_completed(res):
        iteration += 1
        log_file.write(exp_name + " : " + str(iteration) + "/" + str(len(commands)) + " completed\n")
        log_file.flush()
    log_file.write("End experiment " + exp_name + "\n")
    log_file.close()


def launch_experiment_many_measure_sets(exp, exp_name):
    commands = []
    for dataset, measures in zip(exp["datasets"], exp["measures"]):
        exp_copy = exp.copy()
        exp_copy["datasets"] = [dataset]
        exp_copy["measures"] = measures
        commands += [make_command(config) for config in make_configs(exp_copy)]
    executor = futures.ThreadPoolExecutor(max_workers=exp["npr"])
    res = [executor.submit(launch_command, command) for command in commands]
    iteration = 0
    log_file = open(project_log_file, 'a')
    log_file.write("Start experiment " + exp_name + "\n")
    for f in futures.as_completed(res):
        iteration += 1
        log_file.write(exp_name + " : " + str(iteration) + "/" + str(len(commands)) + " completed\n")
        log_file.flush()
    log_file.write("End experiment " + exp_name + "\n")
    log_file.close()



def make_aetheris_command(dataset, pm, am, class_aware, result_path, subcommand):
    data_path = os.path.join(project_data_dir, dataset)
    aetheris_path = os.path.join(project_scripts_dir, "aetheris.py")
    return ["python3", aetheris_path, subcommand, data_path, result_path, pm, am, '-c' if class_aware else '']


def launch_aetheris_process(command, to):
    res = {}
    command_str = " ".join(command)
    try:
        print("Start " + command_str)
        process = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=to, check=True)
        print("End " + command_str)
        res = json.loads(process.stdout.decode("UTF-8"))
    except subprocess.TimeoutExpired:
        print("Timeout " + command_str)
        res = {'stderr': 'Timeout expired'}
    except subprocess.CalledProcessError as e:
        print("Called process error " + command_str)
        res = {'stderr': e.stderr.decode("UTF-8")}
    finally:
        with open(command[3], 'w') as json_result:
            json_result.write(json.dumps(res))


def clean_tmp_res():
    tmp_list = list(filter(lambda f: ".tmp" in f, os.listdir(project_res_dir)))
    for file in tmp_list:
        os.remove(os.path.join(project_res_dir, file))


def call_micmac_process(dataset, pm, am, class_aware, result_path, time_limit):
    try:
        print("Call micmac for " + dataset + ", measures: " + pm + am)
        command = make_aetheris_command(dataset, pm, am, class_aware, result_path, "micmac")
        start = time.time()
        subprocess.run(command, check=True, timeout=time_limit)
        end = time.time() - start
        print("End micmac for " + dataset + ", measures: " + pm + am, ", time : " + str(round(end, 2)) + "s")
        return end
    except subprocess.CalledProcessError:
        print("CalledProcessError in micmac for " + dataset + ", measures: " + pm + am)
        return -1
    except subprocess.TimeoutExpired:
        print("TimeoutError in micmac for " + dataset + ", measures: " + pm + am)
        return time_limit + 1


def call_micmac_process_json(dataset, pm, am, class_aware, result_path, time_limit, thr, json_path):
    try:
        print("Call micmac for " + dataset + ", measures: " + pm + am )
        command = make_aetheris_command(dataset, pm, am, class_aware, result_path, "micmac")
        command += [str(thr)]
        print(" ".join(command))
        start = time.time()
        process = subprocess.run(command, check=True, timeout=time_limit, stdout=subprocess.PIPE)
        end = time.time() - start
        print("End micmac for " + dataset + ", measures: " + pm + am, ", time : " + str(round(end, 2)) + "s")
        res = json.loads(process.stdout.decode("UTF-8"))
        res["timeCount"] = round(end, 2)
        print(res)
        write_json(json_path, res)
    except subprocess.CalledProcessError:
        print("CalledProcessError in micmac for " + dataset + ", measures: " + pm + am)
        write_json(json_path, {'stderr': 'CalledProcessError'})
    except subprocess.TimeoutExpired:
        print("TimeoutError in micmac for " + dataset + ", measures: " + pm + am)
        write_json(json_path, {'stderr': 'Timeout'})


def write_json(path, content):
    with open(path, 'w') as f:
        f.write(json.dumps(content))


def call_aetheris_process(dataset, pm, am, class_aware, result_path, closed_path, time_limit, micmac_time):
    if micmac_time == -1:
        write_json(result_path, {'stderr': 'Error micmac'})
        return
    if micmac_time > time_limit:
        write_json(result_path, {'stderr': 'Timeout expired for micmac'})
        return
    try:
        print("Call aetheris for " + dataset + ", measures: " + pm + am)
        command = make_aetheris_command(dataset, pm, am, class_aware, closed_path, "aetheris")
        start = time.time()
        process = subprocess.run(command, timeout=int(time_limit - micmac_time), check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print(process.stderr.decode("UTF-8"))
        total_time = micmac_time + time.time() - start
        res = json.loads(process.stdout.decode("UTF-8"))
        res["timeCount"] = round(total_time, 2)
        res["searchState"] = "TERMINATED"
        write_json(result_path, res)
        print("End aetheris for " + dataset + ", measures: " + pm + am + ", skypatterns found in " + str(round(total_time, 2)) + "s")
    except subprocess.CalledProcessError:
        print("CalledProcessError in aetheris for " + dataset + ", measures: " + pm + am)
        write_json(result_path, {'stderr': 'Error with aetheris'})
    except subprocess.TimeoutExpired:
        print("TimeoutError in aetheris for " + dataset + ", measures: " + pm + am)
        write_json(result_path, {'stderr': 'Timeout expired for aetheris'})


def launch_aetheris_exp(exp):
    executor = futures.ThreadPoolExecutor(max_workers=exp["npr"])
    commands = []
    to = exp["timelimit"]
    micmac_time = dict()
    for dataset in exp["datasets"]:
        for m in exp["measures"]:
            class_aware = not exp["noclasses"]
            pm = m[0]
            am = m[1] if len(m) > 1 else ""
            sky_m = re.sub("\n", "", subprocess.run(["python3", os.path.join(project_scripts_dir, "aetheris.py"), "max_convert", pm, am, "-c" if class_aware else ""], stdout=subprocess.PIPE).stdout.decode("UTF-8"))
            c = 'classes' if class_aware else 'noclasses'
            closed_path = os.path.join(project_res_dir, "closed_" + Path(dataset).stem + "_" + sky_m + ".tmp")
            if not (dataset + sky_m) in micmac_time:
                micmac_time[dataset + sky_m] = executor.submit(call_micmac_process, dataset, pm, am, class_aware, closed_path, to)
            # if micmac_time[dataset + sky_m] != -1:
            #     call_aetheris_process()
            # commands.append(make_aetheris_command(dataset, pm, am, class_aware, result_path))
    # res = [executor.submit(launch_aetheris_process, command, to) for command in commands]
    for r in list(micmac_time.values()):
        r.result()
    sky_search = []
    for dataset in exp["datasets"]:
        for m in exp["measures"]:
            class_aware = not exp["noclasses"]
            pm = m[0]
            am = m[1] if len(m) > 1 else ""
            sky_m = re.sub("\n", "", subprocess.run(["python3", os.path.join(project_scripts_dir, "aetheris.py"), "max_convert", pm, am, "-c" if class_aware else ""], stdout=subprocess.PIPE).stdout.decode("UTF-8"))
            c = 'classes' if class_aware else 'noclasses'
            closed_path = os.path.join(project_res_dir, "closed_" + Path(dataset).stem + "_" + sky_m + ".tmp")
            result_path = os.path.join(project_res_dir, Path(dataset).stem + '-aetheris-' + pm + am + '-' + str(
                to) + 's' + '-' + c + '.json')
            sky_search.append(executor.submit(call_aetheris_process, dataset, pm, am, class_aware, result_path, closed_path, to, micmac_time[dataset + sky_m].result()))
    for r in sky_search:
        r.result()
    clean_tmp_res()


def launch_micmac_exp(exp):
    executor = futures.ThreadPoolExecutor(max_workers=exp["npr"])
    res = []
    to = exp["timelimit"]
    for dataset in exp["datasets"]:
        for m in exp["measures"]:
            class_aware = not dataset_infos[os.path.splitext(dataset)[0] + ".dat"][noclasses]
            pm = m[0]
            am = m[1] if len(m) > 1 else ""
            c = 'classes' if class_aware else 'noclasses'
            for t in dataset_infos[os.path.splitext(dataset)[0] + ".dat"][threshold]:
                closed_path = os.path.join(project_res_dir, "closed_" + Path(dataset).stem + "_" + pm + am + "_" + str(t) + ".tmp")
                json_path = os.path.join(project_res_dir, Path(dataset).stem + '-micmac-' + pm + am + '-' + str(
                to) + 's' + '-' + c + "-" + str(t) + '.json')
                res.append(executor.submit(call_micmac_process_json, dataset, pm, am, class_aware, closed_path, to, t, json_path))
    for r in res:
        r.result()
    clean_tmp_res()


project_res_ar_dir = os.path.abspath(os.path.join(project_dir, "results_ar"))
ar_mining_jar = os.path.abspath(os.path.join(project_dir, "target", "ar-0.0.1-jar-with-dependencies.jar"))


def make_mnr_command(dataset, use_case):
    dataset_path = os.path.abspath(os.path.join(project_data_dir, dataset))
    dataset_name = dataset.split(".")[0]
    skypattern_file = os.path.abspath(os.path.join(project_res_dir, dataset_name +
                                                   "-closedsky-fat-mincov-86400s-closedsky-noclasses-wc.json"))
    res_file = os.path.abspath(os.path.join(project_res_ar_dir, dataset_name))
    return [java_path, "-jar", "-Xmx20480m", ar_mining_jar, "-d", dataset_path, "-s", skypattern_file, "-r", res_file,
            "--uc", str(use_case), "--tl", "3600"]


def start_mnr_command(command):
    print("start " + " ".join(command))
    subprocess.run(command)
    print("end " + " ".join(command))


def launch_exp_mnr(exp):
    executor = futures.ThreadPoolExecutor(max_workers=exp["npr"])
    for dataset in exp["datasets"]:
        for use_case in [0, 1]:
            command = make_mnr_command(dataset, use_case)
            executor.submit(start_mnr_command,  command)


def make_commands_exp_sky(exp):
    commands = []
    for dataset in exp["datasets"]:
        for m in exp["measures"]:
            for subcommand, wc in zip(exp["subcommands"], exp["wc"]):
                config = {
                    "data": os.path.join(project_data_dir, dataset),
                    "subcommand": subcommand,
                    "pmeasures": m[0],
                    "ameasures": m[1] if len(m) > 1 else "",
                    "strategy": exp["strategy"],
                    "timelimit": str(exp["timelimit"]),
                    "patterntype": exp["patterntype"],
                    "noclasses": dataset_infos[dataset][noclasses] if "noclasses" not in exp else exp["noclasses"],
                }
                if "cst" in exp:
                    config["cst"] = exp["cst"]
                if wc:
                    config["wc"] = True
                if "savepatterns" in exp:
                    config["savepatterns"] = True
                commands.append(make_command(config))
    return commands


def launch_process(command):
    command_str = " ".join(command)
    print("start " + command_str)
    subprocess.run(command)
    print("end " + command_str)


def launch_exp(commands, npr):
    res = []
    executor = futures.ThreadPoolExecutor(max_workers=npr)
    for command in commands:
        res.append(executor.submit(launch_process, command))
    for r in res:
        r.result()


def make_mnr_command(dataset_path, time_limit, res_path, constraints):
    command = [java_path, "-jar", project_jar, "arm", "-d", dataset_path, "--tl", str(time_limit), "--csv", res_path,
               "--sr", "--rt", "mnr"]
    if len(constraints) > 0:
        for constraint in constraints:
            command += ["--cst", constraint]
    return command


def compute_min_freq_and_conf(sky_path):
    patterns = parse_json_patterns(sky_path)
    min_conf = 10000
    min_freq = 9999999
    for p in patterns:
        if p.measures[0] < min_freq:
            min_freq = p.measures[0]
        if p.measures[2] < min_conf:
            min_conf = p.measures[2]
    return min_freq, min_conf / 10000


def make_commands_exp_mnr(exp):
    commands = []
    for dataset in exp["datasets"]:
        dataset_without_suffix = dataset.split(".")[0]
        dataset_path = os.path.abspath(os.path.join(project_data_dir, dataset))
        time_limit = exp["timelimit"]
        res_path = os.path.abspath(os.path.join(project_dir, "results_ar", dataset_without_suffix + "_sky"))
        sky_path = os.path.abspath(os.path.join(project_res_dir, dataset_without_suffix + exp["suffix"]))
        constraints = ["sky=" + sky_path]
        commands.append(make_mnr_command(dataset_path, time_limit, res_path, constraints))
        res_path = os.path.abspath(os.path.join(project_dir, "results_ar", dataset_without_suffix + "_all"))
        min_freq, min_conf = compute_min_freq_and_conf(sky_path)
        constraints = ["fmin=" + str(min_freq), "cmin=" + str(min_conf)]
        commands.append(make_mnr_command(dataset_path, time_limit, res_path, constraints))
    return commands
