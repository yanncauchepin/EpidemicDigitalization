# Epidemic Digitalization #
> ### Language : Python ###

## Summary ##

The aim of this project was to use reinforcement learning to optimize the management of an epidemic crisis. The interest is to produce a multicriteria optimization by limiting the infectious exchanges of an epidemic and by maximizing the economic stability of a territory. This project was carried out in a complete autonomy and had to be imagined without any guide.

From an openstreetmap file, we get the mapping of any territory. According to several strategies, it is accessible to match it with demographic data. Each database has its own appropriate design and specific attributes to make digitalization as realistic as possible. This is what we can call "static digitalization".

The "dynamic digitalization" corresponds to the elaboration of the scripts of a day, where each individual travels a set of places with some timings. This part is very complex and must reproduce the diversity of daily routine, with some atypical scripts. With the use of SumoMobility implementation, we can reproduce urban traffic of each script with as much realism as possible.

We can add several layers of evaluations to obtain individualized scores for each individual and place, at the end of each day. By combining control actions on the various facets of digitalization, we can edit these scripts to better manage the digitalized society. On a predetermined time step, we can then carry out infectious and economic evaluations that will be used in a reinforcement learning algorithm.

The infectious design is carried out by considering the different states, real and/or identified, of the individuals. The contamination of individuals is modeled by the accumulation of contagious particles in an organism with a certain threshold. The evolution of the states is realized by using probabilistic laws and antigen/antibody modeling.

By linking global data together, we can reproduce the functioning of a black-box that digitizes any territory and allows us to optimize its functioning.

This project was realised during an internship at the **University of Luxembourg**. One of the main technologies used was ***OpenStreetMap*** and ***SumoMobility***.

## Prerequisites ##

Before running this code, ensure you have the following :

- Python packages described in ***requirements.txt***.

## Usage ##

### Example ###

## Results ##

## To do list ##

- [ ] Check and upgrade code.
- [ ] Complete a to do list.
- [ ] Complete README.
- [ ] Adapt the repository to well developer traditions.
