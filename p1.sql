use bmi_25dec21;
delimiter $$
drop trigger if exists t1$$
create trigger t1 before insert on person for each row
begin
if new.name is null or length(new.name)<2 or new.name regexp '[^A-Za-z ]' then
	signal SQLSTATE '19209' set message_text="Name should have atleast 2 alphabets";
end if;

if new.height is null or new.height<0.305 or new.height>2.413 then
	signal SQLSTATE '57134' set message_text="Height should be a +ve number between 0.305 and 2.413 metres only";
end if;

if new.weight is null or new.weight<=0 or new.weight>120 then
	signal SQLSTATE '46864' set message_text="Weight should be between 1 and 120 kgs only";
end if;

if new.phone is null or length(new.phone)!=10 or new.phone<=0 then
	signal SQLSTATE '62773' set message_text="Phone number should be +ve and must have 10 digits only";
end if;

if new.age is null or new.age<=0 or new.age>100 then
	signal SQLSTATE '48543' set message_text="Age should be between 1 and 100 years";
end if;
end $$
delimiter ;