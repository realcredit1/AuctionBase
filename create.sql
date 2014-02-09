create table Item (itemID string PRIMARY KEY, 
	name string, 
	currently string, 
	buy_price string, 
	first_bid string, 
	started string, 
	ends string, 
	userID string references User, 
	description string, 
	constraint ch_buy_price check buy_price >= first_bid,
	constraint );
create table User (userID string PRIMARY KEY, rating string, location string, country string);
create table Category (itemID string references Item, category string, PRIMARY KEY (itemID, category));
create table Bid (itemID string references Item, userID string references User, time string, amount string, PRIMARY KEY (itemID,time));
