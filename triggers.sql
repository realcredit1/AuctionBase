/*
 * File: triggers.sql
 * All bids are on "open" auctions (after start time and before end time)
 */

create trigger time_insert
before insert on Time
begin
	raise(abort, 'Error: Time may not contain more than one tuple');
end;

create trigger time_delete
before delete on Time
begin
	raise(abort, 'Error: Cannot delete from table Time');
end;

create trigger time_update
before update on Time
when New.currtime < Old.currtime
begin
	raise(abort, 'Error: Backwards movement in time not permitted');
end;


-- BID
-- bids can only be inserted at the current time
create trigger bid_insert
before insert on Bid
when Bid.time != Time.currtime
begin
	raise(abort, 'Error: Bids can only be made at the current time');
end;

create trigger bid_update
before update on Bid
begin
	raise(abort, 'Error: Cannot update bids');
end;

create trigger bid_delete
before update on Bid
begin
	raise(abort, 'Error: Cannot delete bids');
end;

-- no simultaneous bids, therefore every new bid increments Time


	
-- users cannot bid on their own item


-- ITEM
-- users

create trigger item_insert
before insert on Item
