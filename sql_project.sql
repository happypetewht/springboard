/* Welcome to the SQL mini project. For this project, you will use
Springboard' online SQL platform, which you can log into through the
following link:

https://sql.springboard.com/
Username: student
Password: learn_sql@springboard

The data you need is in the "country_club" database. This database
contains 3 tables:
    i) the "Bookings" table,
    ii) the "Facilities" table, and
    iii) the "Members" table.

Note that, if you need to, you can also download these tables locally.

In the mini project, you'll be asked a series of questions. You can
solve them using the platform, but for the final deliverable,
paste the code for each solution into this script, and upload it
to your GitHub.

Before starting with the questions, feel free to take your time,
exploring the data, and getting acquainted with the 3 tables. */



/* Q1: Some of the facilities charge a fee to members, but some do not.
Please list the names of the facilities that do. */

Code: 
SELECT name
  FROM country_club.Facilities
 WHERE membercost = 0.0


/* Q2: How many facilities do not charge a fee to members? */

Code:
SELECT COUNT(name)
  FROM country_club.Facilities
 WHERE membercost = 0.0



/* Q3: How can you produce a list of facilities that charge a fee to members,
where the fee is less than 20% of the facility's monthly maintenance cost?
Return the facid, facility name, member cost, and monthly maintenance of the
facilities in question. */

Code:
SELECT facid,
       name,
       membercost,
       monthlymaintenance
  FROM country_club.Facilities
 WHERE membercost  < monthlymaintenance * 0.2 


/* Q4: How can you retrieve the details of facilities with ID 1 and 5?
Write the query without using the OR operator. */

Code:
SELECT *
  FROM country_club.Facilities
WHERE facid in (1, 5)


/* Q5: How can you produce a list of facilities, with each labelled as
'cheap' or 'expensive', depending on if their monthly maintenance cost is
more than $100? Return the name and monthly maintenance of the facilities
in question. */

Code:
SELECT facid,
       monthlymaintenance,
       (CASE WHEN monthlymaintenance <= 100 
        THEN 'cheap' ELSE 'expensive' END) AS greater_than_100       
  FROM country_club.Facilities



/* Q6: You'd like to get the first and last name of the last member(s)
who signed up. Do not use the LIMIT clause for your solution. */

Code:
SELECT firstname, surname
 FROM country_club.Members
WHERE joindate = (SELECT MAX(joindate)
                  FROM Members
                 )


/* Q7: How can you produce a list of all members who have used a tennis court?
Include in your output the name of the court, and the name of the member
formatted as a single column. Ensure no duplicate data, and order by
the member name. */

Code:
SELECT DISTINCT CONCAT(Members.firstname, ' ', Members.surname) AS member_name, 
             Facilities.name AS facility_name
  FROM country_club.Bookings
INNER JOIN country_club.Facilities
    ON Bookings.facid = Facilities.facid
INNER JOIN country_club.Members
    ON Bookings.memid = Members.memid
WHERE Bookings.facid IN (0, 1)


/* Q8: How can you produce a list of bookings on the day of 2012-09-14 which
will cost the member (or guest) more than $30? Remember that guests have
different costs to members (the listed costs are per half-hour 'slot'), and
the guest user's ID is always 0. Include in your output the name of the
facility, the name of the member formatted as a single column, and the cost.
Order by descending cost, and do not use any subqueries. */

Code:
SELECT CONCAT(Members.firstname, ' ', Members.surname) AS member_name, 
       Facilities.name AS facility_name,
       CASE WHEN Members.surname = 'GUEST' THEN Bookings.slots * Facilities.guestcost
       ELSE Bookings.slots * Facilities.membercost END AS cost 
  FROM country_club.Bookings
INNER JOIN country_club.Facilities
    ON Bookings.facid = Facilities.facid
INNER JOIN country_club.Members
    ON Bookings.memid = Members.memid
WHERE Bookings.starttime BETWEEN '2012-09-14 00:00:00' AND '2012-09-14 23:59:59'
HAVING cost > 30.0
ORDER BY cost DESC


/* Q9: This time, produce the same result as in Q8, but using a subquery. */

Code:
SELECT
      (SELECT CONCAT(M.firstname, ' ', M.surname)) AS member_name,
      (SELECT F.name) AS facilities_name,
      (SELECT CASE WHEN M.firstname = 'GUEST' THEN F.guestcost * B.slots
       ELSE F.membercost * B.slots END) AS cost
  FROM country_club.Bookings B JOIN country_club.Members M
                                 ON B.memid = M.memid
                               JOIN country_club.Facilities F
                                 ON B.facid = F.facid
WHERE B.starttime BETWEEN '2012-09-14 00:00:00' AND '2012-09-14 23:59:59'
      AND (SELECT CASE WHEN M.firstname = 'GUEST' THEN F.guestcost * B.slots
       ELSE F.membercost * B.slots END) > 30.0
ORDER BY cost DESC


/* Q10: Produce a list of facilities with a total revenue less than 1000.
The output of facility name and total revenue, sorted by revenue. Remember
that there's a different cost for guests and members! */

Code:

SELECT F.name AS facilities_name,
      SUM(CASE WHEN M.firstname = 'GUEST' THEN F.guestcost * B.slots
       ELSE F.membercost * B.slots END) AS revenue
  FROM country_club.Bookings B JOIN country_club.Members M
                                 ON B.memid = M.memid
                               JOIN country_club.Facilities F
                                 ON B.facid = F.facid
GROUP BY F.name
HAVING revenue <1000.0
ORDER BY revenue DESC

