Readme File:

- Introduction to Code Architecture:

I've used python for programming Naive bayes algorithm and used the concept of classes, functions, list/dictionaries, loops and data frames in python to achieve this. 

- Data Pruning and Error Handling

I've also done data cleaning and pruning in the steps. for e.g: in case of true and false, i've stored it as string, other special characters are also being handled and converted into strings so that they won't give any error. While comparing in data frame, they are matched and converted to their respective types.

- Bonus part Explaination:
I've taken the student dataset from the links mentioned in the assignment, and ran three classifiers: Naive Bayes, ID3 and C4.5.
ID3 and C4.5 classfieres are run through weka. The results comparison along with the proper screenshots are stored in a separate file called BonusSection.PDF.
Link to Dataset: https://archive.ics.uci.edu/ml/datasets/Student+Performance

- Overview of the program code:
	
  There is one single Python file named as NaiveBayes.py


- The following is the  program structure:

   main()---->ask for input
   			---->filename for Training set. [If file doen't exist, you will get a validation error]
   			---->Filename for Test data set [If file doen't exist, you will get a validation error]
   			---->After you enter the correct datasets, program will give you the options to select one Target Attribute

   		----> loaddb
   			---->I have used the concept of Dataframe to load and store data in python.

   		---->Now the program will train the data set and Calculate the probabilities of individual items 
            ----> Formulae for Probability: P(A/B) = ( P(B/A)* P(A) ) / P(B) 
            ----> Store the result in a dictionary

   		---->Run the test on Test Dataset
   			----> Loop over Test dataset
            ----> Select the best value according to the probabilities calculated in Train Dataset.
            ----> Classify

   		---->file Write()
   			---->if file exist then delete
   			---->create new file and write
   			
- Run the program:
   	bluenose: python NaiveBayes.py
   	
- The result is stored in the file: /users/grad/bhalla/assign5/Output.txt , to view the result:                         
   bluenose: more Output.txt   
- If you want to change the file output path: Open the file in text edittor and change the value for variable "Path".




