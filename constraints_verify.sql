/* 
 * File: constraints_verify.sql
 *
 * SQL queries (using SQLite) to test that the initial data bulk-loaded
 * without constraint-checking conforms to certain referential integrity
 * constraints, and certain other constraints which will be protected from
 * modifications to the database by triggers.
 *
 */

-- Referential Integrity
select itemID from Category where itemID not in (select itemID from Item);
select itemID from Bid where itemID not in (select itemID from Item);
select userID from Bid where userID not in (select userID from User);
select userID from Item where userID not in (select userID from User);

-- Row-Level Check
-- start time is before end time
select * from Item where (started > ends);
-- buy price is greater than first bid
select * from Item where (buy_price < first_bid);
-- first bid is greater than zero
select * from Item where (first_bid <= 0);

-- Triggers:
-- cannot place bid on own item
select * from Bid natural join Item where (Bid.userID == Item.userID);
-- !!! all bids occur before current time
select * from Bid where time > (select currtime from Time);
-- no bids on closed auctions
select * from Bid join Item on (Bid.itemID == Item.itemID) where (time < started);
select * from Bid join Item on (Bid.itemID == Item.itemID) where (time > ends);
-- no bids greater than buy price
select * from Bid join Item on (Bid.itemID == Item.itemID) where (amount > buy_price);
-- all bids must be greater than starting price
select * from Bid join Item on (Bid.itemID == Item.itemID) where(amount < first_bid);
-- bids on one item must increase in amount over time
select * from Bid B1 join Bid B2 on (B1.itemID == B2.itemID) where(B1.time > B2.time and B1.amount < B2.amount);
-- current price of item is amount of most recent Bid
select * from (select Item.itemID, Item.currently, max(Bid.amount) as maxBid from Item join Bid on (Item.itemID == Bid.itemID) group by Item.itemID) where (currently != maxBid);
-- if no bids, currently = first_bid
select * from Item where (itemID not in (select itemID from Bid)) and (currently != first_bid);