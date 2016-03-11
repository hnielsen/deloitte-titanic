import csv as csv
import numpy as np

csv_file_object = csv.reader(open('data/train.csv', 'rb'))       # Load in the csv file
header = csv_file_object.next()                             # Skip the fist line as it is a header
data=[]                                                     # Create a variable to hold the data

for row in csv_file_object:                 # Skip through each row in the csv file
	data.append(row)                        # adding each row to the data variable

data = np.array(data)                       # Then convert from a list to an array

fare_ceiling = 40
# then modify the data in the Fare column to = 39, if it is greater or equal to the ceiling
data[ data[0::,9].astype(np.float) >= fare_ceiling, 9 ] = fare_ceiling - 1.0

fare_bracket_size = 10
number_of_price_brackets = fare_ceiling / fare_bracket_size
number_of_classes = 3                             # I know there were 1st, 2nd and 3rd classes on board.
number_of_classes = len(np.unique(data[0::,2]))   # But it's better practice to calculate this from the Pclass directly:
												  # just take the length of an array of UNIQUE values in column index 2

survival_table = np.zeros([2,number_of_classes,number_of_price_brackets],float)

# I can now find the stats of all the women and men on board
for i in xrange(number_of_classes):
	for j in xrange(number_of_price_brackets):
		women_only_stats = data[ (data[0::,4] == "female") \
								 & (data[0::,2].astype(np.float) == i+1) \
								 & (data[0:,9].astype(np.float) >= j*fare_bracket_size) \
								 & (data[0:,9].astype(np.float) < (j+1)*fare_bracket_size), 1]
		men_only_stats = data[ (data[0::,4] != "female") \
								 & (data[0::,2].astype(np.float) == i+1) \
								 & (data[0:,9].astype(np.float) >= j*fare_bracket_size) \
								 & (data[0:,9].astype(np.float) < (j+1)*fare_bracket_size), 1]
		survival_table[0,i,j] = np.mean(women_only_stats.astype(np.float))  # Female stats
		survival_table[1,i,j] = np.mean(men_only_stats.astype(np.float))    # Male stats

# Since in python if it tries to find the mean of an array with nothing in it
# (such that the denominator is 0), then it returns nan, we can convert these to 0
# by just saying where does the array not equal the array, and set these to 0.
survival_table[ survival_table != survival_table ] = 0.

# Now I have my proportion of survivors, simply round them such that if <0.5
# I predict they dont surivive, and if >= 0.5 they do
survival_table[ survival_table < 0.5 ] = 0
survival_table[ survival_table >= 0.5 ] = 1

# Now I have my indicator I can read in the test file and write out
# if a women then survived(1) if a man then did not survived (0)
# First read in test
test_file = open('./data/test.csv', 'rb')
test_file_object = csv.reader(test_file)
header = test_file_object.next()

# Also open the a new file so I can write to it.
predictions_file = open("genderclassmodel.csv", "wb")
predictions_file_object = csv.writer(predictions_file)
predictions_file_object.writerow(["PassengerId", "Survived"])

# First thing to do is bin up the price file
for row in test_file_object:
	for j in xrange(number_of_price_brackets):
		# If there is no fare then place the price of the ticket according to class
		# No fare recorded will come up as a string so try to make it a float
		try:
			row[8] = float(row[8])
		# If fails then just bin the fare according to the class
		except:
			bin_fare = 3 - float(row[1])
			break                     # Break from the loop and move to the next row
		# Otherwise now test to see if it is higher than the fare ceiling we set earlier
		if row[8] > fare_ceiling:
			bin_fare = number_of_price_brackets - 1
			break                     # And then break to the next row
		# If passed these tests then loop through each bin until you find the right one
		# append it to the bin_fare and move to the next loop
		if row[8] >= j*fare_bracket_size and row[8] < (j+1)*fare_bracket_size:
			bin_fare = j
			break
	# Now I have the binned fare, passenger class, and whether female or male, we can
	# just cross ref their details with our survival table
	if row[3] == 'female':
		predictions_file_object.writerow([row[0], "%d" % int(survival_table[ 0, float(row[1]) - 1, bin_fare ])])
	else:
		predictions_file_object.writerow([row[0], "%d" % int(survival_table[ 1, float(row[1]) - 1, bin_fare])])

# Close out the files
test_file.close()
predictions_file.close()
