-- all players that play QB
-- Q1
select nameFull
from players
where position = "QB";

-- players under 6 feet
-- Q2
select nameFull
from players
where heightInches <= 72;

-- receivers that made a pass
-- Q3
select distinct nameFull
from players as PL, passer as PR
where PR.playerId = PL.playerId
    and PR.passPosition = "WR"
    and PR.passComp = 1;

-- runners with at least 7 TDs
-- Q4
select P.nameFull as Players
from players as P, rusher as RS
where P.playerID = RS.playerID
    and P.position = "RB"
group by P.playerID
having count(RS.rushTd) >= 7;

-- games with a final score difference less than one touchdown
-- Q5
select season, week, winningTeam
from games
where (homeTeamFinalScore - visitingTeamFinalScore) < 6;


-- entering new players into tables
-- Q6
insert into players values(99999999, "John Doe", "LB", 73, 240, "1999-01-01");

-- update players weight
-- Q7
update players
set weight = 245
where playerID = 99999999;

-- checking to see if updates worked
-- Q8
select *
from players
where playerId = 99999999;

-- players that have both a rushing and no receiving fumbles
-- Q9
select distinct nameFull
from players as P, rusher as RB, receiver as RS
where P.playerID = RB.playerID
    and RB.playerID = RS.playerID
    and RB.rushTD >= 1;

-- player that are 30
-- Q10
select nameFull, dob
from players
where dob like "%1990";

--Lbs with a pick and 5 sacks
-- Q11
select nameFull
from interceptions as I, sacks as S, players as P
where I.playerId = S.playerId
    and P.playerId = I.playerId
    and S.sackNull = 0
    and sackPosition = "LB"
    and I.intPosition = "LB"
    and I.int = 1
    and I.intNull = 0
group by I.playerId
having count(S.sackNull) = 5;

-- players with most solo tackles in a team
-- Q12
select T1.playerId, sum(T1.tackleYdsScrim)
from tackles as T1, tackles as T2
where T1.teamId = T2.teamId
    and T1.playerId != T2.playerId
group by T1.teamId
order by sum(T1.tackleYdsScrim) desc;

-- players with pass defenses and sacks
-- Q13
select P.nameFull, P.playerId
from players as P, passDef as I, 
        (SELECT playerId
            from sacks
            where sackNull = 0
            group by playerId
            having count(sackId) >= 1) as F
where F.playerId = I.playerId
    and I.passDefNull = 0
    and F.playerId = P.playerId
group by F.playerId
having count(I.passDefId) >= 1;

-- remove entries
-- Q14
delete from plays
where playId = 30298;

-- teams in 2004 that played in the playoffs
-- Q15
select homeTeamId, visitorTeamId
from games
where seasonType != "PRE" 
    and seasonType != "REG"
    and season = 2004;

-- winners of superbowls
-- Q16
select season, winningTeam
from games
where seasonType = "SB";

-- players that had a forced turnover
-- Q17
select playerId
from fumbles
where fumType = "forced"
    and fumTurnover = 1
    and fumNull = 0
group by playerId
UNION
select playerId
from interceptions as I
where I.intNull = 0
    and I.int = 1
group by playerId;

-- players with a rushing touchdown to the left side and a catch
-- Q18
select playerId
from receiver
where recNull = 0
    and rec = 1
    and recEnd = "in bounds"
group by playerId
INTERSECT
select playerId
from rusher
where rushDirection = "left"
    and rushPrimary = 1
    and rushTd = 1
    and rushNull = 0
group by playerId;

-- players that had a TD called back by penatly
-- Q19
select playerId
from rusher
where rushPrimary = 1
    and rushTd = 1
    and rushNull = 1;

-- total rushing yards in a game
-- Q20
select G.gameId, sum(rushYards) as home
from games as G, rusher as R, plays as P
where G.gameId = P.gameId
    and P.playId = R.playId
    and G.homeTeamId = R.teamId
UNION
select G.gameId, sum(rushYards) as visitors
from games as G, rusher as R, plays as P
where G.gameId = P.gameId
    and P.playId = R.playId
    and G.visitorTeamId = R.teamId;