# Simmerpop
Simmulation of Emergent Populations

## Description
Simmerpop is a repository of code for conducting virtual life simmulations. It was developed with a focus on simmulating early life ecosystems to further our understanding of the origin of life. 

## Usage
To run the simmulation, copy the entire code repository to the desired location on your machine. Then run the python 3 script from the repository's root directory. 

Mac
- Run the python script: python3 run_model.py [arguments value]
- Options:
1. Output folder: output_folder_name [name]
2. Maximum population capacity: POPULATION_CAP [value]. Test values are 500, 1000, 10000
3. Mutation probability: MUTATION_PROB [value]. Test value: 0.005, between 0 and 1. 
4. Horizontal gene transfer probability: HGT_PROB [value]. Test values: 0.1 and 0.5, between 0 and 1. 
5. Number of initial cellularity genes: NUM_CELLGENE [value]. Test values: 0 and 3, between 0 and 8.
6. Energy limit: ENERGY_LIM [value]
+ value == 0: no energy limit
+ value == 1: limit energy abundance to 25% of the maximum population capacity 
+ value == 2: sufficient energy at step 0 and no replenishment over time 

E.g: python3 run_model.py output_folder_name Testing POPULATION_CAP 1000 NUM_CELLGENE 3 ENERGY_LIM 2 

## Support

## Contributing

## Authors and acknowledgment
Yuta A. Takagi, Diep H. Nguyen, Tom Wexler, Aaron D. Goldman

Funding for this work was provided by the National Aeronautics and Space Administration, grants 16-IDEAS16-0001 and 80NSSC19M0069, and the National Science Foundation, grant MRI1427949.

## Selected publications
The origin of cellularity and organismal individuality through digital life simulations 

## License

