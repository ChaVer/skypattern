## Command line

Three subcommands are available :

- **cpsky** : to use CP+SKY
- **closedsky** : to use ClosedSky
- **arm** : association rule mining

### ClosedSky / CP+SKY

Two options are required :

- **-d** : specify the path of the dataset
- **-m** : specify the pattern measures to use, the following ones are available : l (length), f (frequency), a (area), g (growth-rate), t (all-confidence). Note that frequency is equivalent to the support measure and length to the size. The all-confidence is given as a percentage * 100 (for instance, an aconf of 9879 means 98,79%).

To use attribute measures, you can specify the option **-v**, the following ones are available : m (min), M (max), n (mean), u (sum).

You can get three types of patterns, by specifying the option **--pt** :

- closed skypatterns : **closedsky** (**default**), /!\ do not confuse the pattern type with the subcommand ClosedSky
- skypatterns : **sky** (not available with closedsky subcommand)
- closed patterns : **closed**

By default, the first item of each transaction is considered as the class of the transaction and is not taken into account to compute the skypatterns. If you want to include class items into skypatterns computing, you can specify the option **--nc**.

To print the results, two options are available : **-p** to simply print the skypatterns and **--fp** to print the skypatterns in a fancy way. If you want to get statistics about the search (i.e. number of nodes/fails/candidate patterns, time to find all the solutions...), you can use the option **-s**.

If you want a visualization of the search tree, you can specify the option **--trace** with path of a dot file. This dot file can be converted to a graphviz graph.

The option **--json** is used to specify path of a json file which will be used to store details about the search. If you want to store all the patterns and their associated measures, you should specify the option **--sp**.

If you want to limit the time of search, you can use the option **--tl** with an integer representing the time limit of the search (in seconds). The state of a stopped search (time limit is reached without completing the search) will be STOPPED while the state of a complete search will be TERMINATED.

Different strategies can be used to branch on the next item variable. The following ones are available :

- occ : it chooses the not instanciated variable with the greatest number of not-entailed propagators
- (min|max)freq : it chooses the not instanciated variable with the lowest (resp. greatest) frequency (i.e. freq(i) is minimal)
- mincov: it chooses the not instanciated variable i such that freq(x⁺ U {i}) is minimal (**default**)
- (min|max)val : it chooses the not instanciated variable with the lowest (resp. greatest) value (val0 file)
- (min|max)norm : it normalises item frequency and values between 0 and 1, compute average between them and chooses the not instanciated variable with the lowest (resp. greatest) average value
- inpord : it chooses variable with respect to their order

You can specify the strategy to branch on item variables with the option **--str**. The value selector strategy is to instanciate variables to their lower bound (i.e. the first time, the variable is instanciated to 0).

The option **--cst** can be used to specify another constraints such as a minimum frequency or a minimum length. For insance, **--cst fmin=5 --cst lmin=2** requires the pattern to have a minimum frequency of 5 and a minimum length of 2. To specify a relative threshold instead of an absolue one, you can use **--cst rfmin=0.01** (in this example, requires the pattern to appears in at least 1% of transactions in the dataset).

With ClosedSky, you can also specify the option **--wc** if you want to use the weaker version of the global constraint Adequate-Closure.

### Association rule mining (arm)

The option **-d** is required to specify the path of the dataset. You can specify the rule type with the option **--rt** (ar or mnr).

Two types of constraints can be specified :

- min frequency/confidence thresholds : **--cst rfmin=0.9 --cst cmin=0.8** means that we want all the rules with a min relative frequency of 90% and a min confidence of 80%
- sky : **--cst mushroom_fat.json** specify the path of a json skypatterns file (see above) to extract the associated MNR

You can specify the option **--csv** to save search stats in a csv file format. Only the search stats will be saved but if the option **--sr** is specified, the rules will be saved in another csv file. For instance, **--csv mushroom --sr** will generate two files : mushroom_stats.csv which contains search stats and mushroom_rules.csv with the extracted rules.

Another available options : **--tl** to specify a time limit, **-p** to print the rules, **-s** to print search stats.

## Examples

In the following, **skym** is equivalent to **java -jar target/skypattern-1-jar-with-dependencies.jar** .

**skym closedsky -d data/mushroom.aet -m fa -v nM -p -s** : all closed skypatterns mined with ClosedSky for the dataset mushroom with the measures set **{freq(x), area(x), mean(x.val0), max(x.val1)}**, printing the skypatterns and search stats (/!\\ the data folder must contain files named mushroom.val0 and mushroom.val1 with the values of each item).

**skym closedsky -d data/mushroom.aet -m fat --nc --cst lmin=2 --wc --json mushroom_fat.json --sp --tl 1000** : all closed skypatterns mined with ClosedSky for the dataset mushroom with the measures set **{freq(x), area(x), aconf(x)}**, including class items in the mining, with a min length of 2, using the weak version of AdequateClosure, saving the search details and the skypatterns in the file mushroom_fat.json, with a time limit set to 1000s.

**skym arm -d data/mushroom.aet --cst sky=mushroom_fat.json --rt mnr --csv mushroom_sky --sr** : mine all the MNR associated to the skypatterns in the file mushroom_fat.json, saving search details and rules in files mushroom_sky_stats.csv and mushroom_sky_rules.csv

**skym arm -d data/mushroom.aet --cst rfmin=0.9 --cst cmin=0.8 --rt mnr -p -s** : mine all the MNR for the mushroom dataset, with a min relative frequency of 90% and a min confidence of 80%, printing the rules and search stats.