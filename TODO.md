- Fix the problem with hardcoded image id changing all the time (Jamie)
# Argparser menu where you choose OS type, example ubuntu18 , ubuntu16 and a method that pulls the latest image id for that OS type

- Seperate the script into multiple scripts, grouping methods that make sense together (Daragh)
# Creating droplets related stuff in one script, pulling info, listing droplets etc in another and so on

- Create a new method for argparser as its in the main function now (Jamie)
# move the logic for the argparser outside of the main function so we can test it

- Modify the existing methods so they are testable (Daragh)
# Follow solid principles, a method should do only one thing, we shouldn't be calling methods within methods when possible as its difficult to test

- Write tests for each method (Daragh)
