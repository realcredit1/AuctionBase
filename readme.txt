Project Part 1 -- Schema and Data
Part A: Examine the XML data files
	- representes specific point in time: December 20th, 2001, 00:00:01

Part B: Design your relational schema
	1. List your relations. Please specify all keys that hold on each relation. You need not specify attribute types at this stage


		Item (ItemID, Name, Currently, Buy_price, First_bid, Started, Ends, UserID, Description)
			key = ItemID
		User (UserID, Rating, Location, Country)
			key = UserID
		Category (ItemID, Category)
			key = (ItemID, Category)
		Bid (ItemID, UserID, time, amount);
			keys = (ItemID,time), (ItemID, amount)

	2. List all completely nontrivial functional dependencies that hold on each relation, excluding those that effectively specify keys.  Don't worry if your answer turns out to be "none".

		Item:
			ItemID -> Name
			ItemID -> Currently
			ItemID -> Buy_price
			ItemID -> First_bid
			ItemID -> Started
			ItemID -> Ends
			ItemID -> UserID
			ItemID -> Description
		User:
			UserID -> Rating
			UserID -> Location
			UserID -> Country
		Category: none
		Bid:
			ItemID time -> UserID
			ItemID time -> amount
			ItemID amount -> time

	3. Are all of your relations in Boyce-Codd Normal Form? If not, either redesign them and start over, or explain why you feel it is advantageous to use non-BCNF relations.

		If a relational schema is in BCNF, then all redundancy based on functional dependency has been removed, although other types of redundancy may still exist.

		A relational schema R is in Boyce-Codd normal form if and only if for every one of its nontrivial dependencies X->Y, X is a superkey for schema R

	4. List all nontrivial multivalued dependencies.

		none

	5. Are all of your relations in Fourth Normal Form? If not, either redesign them and start over, or explain why you feel it is advantageous to use non-4NF relations.

		A table is in 4NF if and only if, for every one of its non-trivial multivalued dependencies X->>Y, X is a superkey


Part C: Write a data transformation program
	Bulk-Loading Data into SQLite Databases
		- The Data File:
			* ".dat" extension
			* sequence of lines, each specifying one tuple
			* specify delimiter
		- Loading
			.separator <separator>
			.import <loadFile> <tableName>
		-Loading NULL values
			* there is no way to make SQLite load a null value
			* first load data with stand-in value, e.g. "NULL", then
			update <table> set <attribute> = null where <attribute> = 'NULL';
	
	Write a program that transforms the XML data into SQLite load files that are consistent with the relational schema you settled on in Part B.  In the parser skeleton, all of the parsing is done for you by invoking Python's xml.dom.minidom. You need to fill in code that processes the internal representation of the XML tree and produces SQLite load files.


	Python skeleton parser code (read comments)
	
	Load file delimiters and file naming
		- data uses "|", so use multicharacter "<>"
	
	Dollar and data/time values
		- to convert from eBay format to SQLite-readable format
		- use provided transformDollar(String) and transformDttm(String)
	
	Duplicate elimination
		- Unix commands for sorting?

	Automating the process
		- create file runParser consisting of possible sorting and single command
		python parser.py <pathToData>


Part D: Load your data into SQLite
	1. Creating your database interactively
	2. Maitaining your database
	3. Automating the process

Part E: Test your SQLite database




PROJECT PART 2 - DATA INTEGRITY
Part A: Current Time

Part B: Constraints and Triggers
	PRIMARY KEY/UNIQUE
		- itemID on every bid corresponds to actual item
		- no auction may have a bid before its start time or after its end time
		- there are no bids after the current time
		- no auction may have two bids at the same time
		- a user may not bid on an item he or she is offering
		- all sellers and bidders must exist as users




Project Part 3: AuctionBase Web Site
Required functionality
	- Ability to manually change the "current time"
	- Ability for auction users to enter bids on open auctions
	- Automatic auction closing. An auction is "open" after its start time and "closed" when its end time is passed or its buy price is reached
	- Ability to see the winner of a closed auction
	- Ability to browse auctions of interest based on some simple input choices such as category, price, and open/closed status
	- Ability to find an (open or closed) auction based on itemID