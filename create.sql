create table Item (itemID string PRIMARY KEY, name string, currently string, buy_price string, first_bid string, started string, ends string, userID string, description string);
create table User (userID string PRIMARY KEY, rating string, location string, country string);
create table Category (itemID string, category string, PRIMARY KEY (itemID, category));
create table Bid (itemID string, userID string, time string, amount string, PRIMARY KEY (itemID,time));
