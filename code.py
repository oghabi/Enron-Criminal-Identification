import os
import csv
import collections
from collections import Counter
from email.parser import Parser


################### Retrieving the 150 emails of the directories ##############
Enron_150_emails = []

for directory, subdirectory, filenames in os.walk("./data/"):
	# print (directory, subdirectory, filenames)

	for subdir in subdirectory:

		filepath = ""
		From_Email_Found = 0

		#Check if "sent" directory exists
		if os.path.isdir( os.path.join(directory, subdir + "/sent/") ):
			filepath = os.path.join(directory, subdir + "/sent/1.")
			From_Email_Found = 1

		#Check if "sent_items" directory exists
		elif os.path.isdir( os.path.join(directory, subdir + "/sent_items/") ):
			From_Email_Found = 1
			filepath = os.path.join(directory, subdir + "/sent_items/1.")

		#Check if "_sent_mail" directory exists
		elif os.path.isdir( os.path.join(directory, subdir + "/_sent_mail/") ): 
			From_Email_Found = 1
			filepath = os.path.join(directory, subdir + "/_sent_mail/1.")

		else:
			print ("Can't find them", subdir)

		# print (filepath)

		if From_Email_Found:
			with open(filepath, "r", encoding = "ISO-8859-1") as f:
				data = f.read()

			email = Parser().parsestr(data)

			# In Kenneth Lay's Sent directory, its all Rosalee Fleming
			# "lay-k" directory
			if email['from'] == "rosalee.fleming@enron.com":
				Enron_150_emails.append( 'kenneth.lay@enron.com' )

			# "hain-m" directory
			elif email['from'] == "lysa.akin@enron.com":
				Enron_150_emails.append( 'mary.hain@enron.com' )

			# "hodge-j" directory
			elif email['from'] == "jenny.helton@enron.com":
				Enron_150_emails.append( 'jeffrey.hodge@enron.com' )

			# "lavorato-j" directory
			elif email['from'] == "angela.mcculloch@enron.com":
				Enron_150_emails.append( 'john.lavorato@enron.com' )

			# "martin-t" directory
			elif email['from'] == 'laura.vuittonet@enron.com':
				Enron_150_emails.append( 'a..martin@enron.com' )

			# "presto-k" directory
			elif email['from'] == 'tamara.black@enron.com':
				Enron_150_emails.append( 'kevin.presto@enron.com' )

			# "shackleton-s" directory
			elif email['from'] == "kaye.ellis@enron.com":
				Enron_150_emails.append( 'sara.shackleton@enron.com' )

			# "skilling-j" directory
			elif email['from'] == 'sherri.reinartz@enron.com':
				Enron_150_emails.append( 'jeff.skilling@enron.com' )

			else:
				Enron_150_emails.append( email['from'] )


	# For “stokley-c” and “harris-s”
	Enron_150_emails.append( "steven.harris@enron.com" )
	Enron_150_emails.append( "chris.stokley@enron.com" )

	break


print (Enron_150_emails, len(subdirectory), len(Enron_150_emails))

##################################################################################

from_email_list = []
to_email_list = []


# All the emails in the dataset
Email_IDs = {}
ID_Counter = 0  #ID of the nodes
Graph = collections.defaultdict(int) # Key is (From_Node, To_Node) and Value is the number of times an email was sent (From_Node to To_Node)


# Only the emails belonging to the 150 released mailboxes
Email_IDs_150 = {}
ID_Counter_150 = 0
Graph_150 = collections.defaultdict(int)


# All Enron related emails
Email_IDs_Enron = {}
ID_Counter_Enron = 0
Graph_Enron = collections.defaultdict(int)


# os.walk goes through all the inner subdirectories, and files
for directory, subdirectory, filenames in os.walk("./data"):
	# print (directory, subdirectory, filenames)
	for filename in filenames:
		if filename != '.DS_Store':

			filepath = os.path.join(directory, filename)
			# print ("Parsing File: ", directory , filename)
			
			# with automatically closes file for you in the end (so no need to do it explicitly)
			with open(filepath, "r", encoding = "ISO-8859-1") as f:
				data = f.read()

			email = Parser().parsestr(data)
			# print ('email from/to: ', email['from'], email['to'] )


			if email['from']:
				from_email_list.append( email['from'] )


			# Both have to be non-None values (sometimes None due to parsing MIME issues) in order to add to Graph
			if email['from'] and email['to']:

				################ Building Whole Graph ###############
				if email['from'] not in Email_IDs:
					Email_IDs[ email['from'] ] = ID_Counter
					ID_Counter += 1


				email_to = email['to']
				# Do the following to put all the emails on a single line without spaces and comma-sep (if there are multiple emails)
				email_to = email_to.replace("\n", "")
				email_to = email_to.replace("\t", "")
				email_to = email_to.replace(" ", "")

				# Get individual emails from the list
				email_to_list = email_to.split(",")

				for email_to in email_to_list:
					if email_to not in Email_IDs:
						Email_IDs[ email_to ] = ID_Counter
						ID_Counter += 1

					# Append node ids & edges to the graph, the value is the weight
					Graph[ (Email_IDs[ email['from'] ], Email_IDs[ email_to ]) ] += 1.0

					to_email_list.append(email_to)
				########################################################

				

				################ Building 150 Email Graph ###############

				# Make sure there is a pair of emails in Enron_150_emails to create an edge
				if email['from'] in Enron_150_emails and any(i in Enron_150_emails for i in email_to_list):

					if email['from'] not in Email_IDs_150:
						Email_IDs_150[ email['from'] ] = ID_Counter_150
						ID_Counter_150 += 1

					for email_to in email_to_list:
						if email_to in Enron_150_emails:

							if email_to not in Email_IDs_150:
								Email_IDs_150[ email_to ] = ID_Counter_150
								ID_Counter_150 += 1

							Graph_150[ (Email_IDs_150[ email['from'] ], Email_IDs_150[ email_to ]) ] += 1.0

				#########################################################


				################ Building Enron Only Email Graph ###############

				# Make sure there is a pair of emails which are both in Enron
				if '@enron.' in email['from'] and any('@enron.' in i for i in email_to_list):

					if email['from'] not in Email_IDs_Enron:
						Email_IDs_Enron[ email['from'] ] = ID_Counter_Enron
						ID_Counter_Enron += 1

					for email_to in email_to_list:
						if '@enron.' in email_to:

							if email_to not in Email_IDs_Enron:
								Email_IDs_Enron[ email_to ] = ID_Counter_Enron
								ID_Counter_Enron += 1

							Graph_Enron[ (Email_IDs_Enron[ email['from'] ], Email_IDs_Enron[ email_to ]) ] += 1.0

				#########################################################




print (Email_IDs)
print (Graph)
print ('Num Nodes: ', ID_Counter)
print ('Num Emails Sent: ', sum(Graph.values()))
print ('----------------------------------------------------')
print (Email_IDs_150)
print (Graph_150)
print ('Num Nodes 150: ', ID_Counter_150)
print ('Num Emails Sent 150: ', sum(Graph_150.values()))
print ('----------------------------------------------------')
print (Email_IDs_Enron)
print (Graph_Enron)
print ('Num Nodes Enron: ', ID_Counter_150)
print ('Num Emails Sent Enron: ', sum(Graph_Enron.values()))


#First line should be Source,Target,Weight
with open("./Graph_Whole_Edges.csv", "w") as f:
		writer = csv.writer(f)
		writer.writerow(("Source","Target", "Weight"))
		for k,v in Graph.items(): 
			# writer.writerow(k)
			writer.writerow((k[0], k[1] ,v))

#First line should be Id,Label
with open("./Graph_Whole_Emails_to_ID.csv", "w") as f:
		writer = csv.writer(f)
		writer.writerow(("Id","Label"))
		for k,v in Email_IDs.items(): 
			writer.writerow((v,k))

###################################################################

#First line should be Source,Target,Weight
with open("./Graph_150_Edges.csv", "w") as f:
		writer = csv.writer(f)
		writer.writerow(("Source","Target", "Weight"))
		for k,v in Graph_150.items(): 
			writer.writerow((k[0], k[1] ,v))

#First line should be Id,Label
with open("./Graph_150_Emails_to_ID.csv", "w") as f:
		writer = csv.writer(f)
		writer.writerow(("Id","Label"))
		for k,v in Email_IDs_150.items(): 
			writer.writerow((v,k))

###################################################################

#First line should be Source,Target,Weight
with open("./Graph_Enron_Edges.csv", "w") as f:
		writer = csv.writer(f)
		writer.writerow(("Source","Target", "Weight"))
		for k,v in Graph_Enron.items(): 
			writer.writerow((k[0], k[1] ,v))

#First line should be Id,Label
with open("./Graph_Enron_Emails_to_ID.csv", "w") as f:
		writer = csv.writer(f)
		writer.writerow(("Id","Label"))
		for k,v in Email_IDs_Enron.items(): 
			writer.writerow((v,k))


# email['subject']
# email.get_payload()

# print("\nTo email adresses: \n")
# print(Counter(to_email_list).most_common(10))

# print("\nFrom email adresses: \n")
# print(Counter(from_email_list).most_common(10))





