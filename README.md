# Summer Data Scientist Data Assessment
## Crime and Education Lab New York
Repository for the Urban Lab Assessment

I took this Assessment from the Crime and Education Lab New York. 

Instructions are the following:  

This exercise is intended to help us see how you approach a standard data processing and statistical analysis task, and for you to demonstrate your thought process and workflow. The scenario described in this task is fictional, but it is indicative of the type of work we do at Crime and Education Lab New York.  

### Background
Back in January 2010, the NYC District Attorney’s (DA’s) Office implemented a program designed to reduce felony re-arrest rates city wide. That is, individuals arrested post-implementation were offered an intervention on the spot, with the hopes of reducing their chance of getting re-arrested for a felony at some point in the future. As their trusted data partner, the DA’s Office has asked you to help them study the program and its rollout.  

### Data
There are two main datasets, arrests.csv and demo.csv. The arrests.csv file contains information on each arrest made from 2008 through 2011, and includes an arrest ID, a person ID, the date of arrest, and whether the arrest was for a misdemeanor or felony crime. The demo.csv file contains demographic data on each person found in the arrest file, including birthdate, gender, and home precinct.  

### Analysis. 

### Part1: Variable Creation
In this section, you’ll create an analysis dataset allowing you to look more closely at arrestees impacted by the program.
1. For the arrests that occurred post-implementation, create the following covariates: • Age
• Gender
• Home precinct
• Law code (misdemeanor or felony)
• Number of prior misdemeanor arrests (in the last 2 years)
• Number of prior felony arrests (in the last 2 years)
• Number of prior misdemeanor arrests (in the last 6 months) • Number of prior felony arrests (in the last 6 months)
2. Generate a binary outcome that measures any felony re-arrest in a 1-year period following the arrest.

### Part2: Statistical Analysis >> Program Evaluation

In order to study the impact of the program, the DA’s Office had randomly selected some precincts to receive the treatment (i.e. intervention). The other precincts serve as control precincts. All individuals who live in a treatment precinct that were arrested post-implementation received the treatment. The treatment assignments can be found in treatment_assignment.csv.
1. We’re only interested in measuring the effect of the program for the first time an individual receives treatment. Limit your analysis dataset from Part 1 to the first post-implementation arrest for each individual.
2. Did the program significantly reduce felony re-arrest in a 12-month follow-up? Is your result robust to covariate inclusion?

