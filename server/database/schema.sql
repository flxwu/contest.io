create table if not exists User (
    userid integer primary key autoincrement,
    username text not null,
    codeforces_handle text not null,
    usertype text not null,
    useremail text,
    avatar_url text,
    date_joined timestamp default current_timestamp not null,
    oauth_token text not null
);

create table if not exists Usergroup (
    groupid integer primary key autoincrement,
    groupname text not null,
    groupadmin integer not null,
    foreign key(groupadmin) references User(userid)    
);

create table if not exists Contest (
    contestcode text primary key not null,
    contestname text not null,
    date_start timestamp not null,
    date_end timestamp not null,
    visible integer default 0
);

create table if not exists Task (
    taskid integer primary key autoincrement,
    taskname text not null,
    -- Json-stringified tags array
    tasktags text not null,
    codeforces_url text not null,
    codeforces_id integer not null,
    codeforces_index text not null
);

create table if not exists in_usergroup (
    usergroup integer not null,
    user integer not null,
    foreign key(usergroup) references Usergroup(groupid),
    foreign key(user) references User(userid),
    primary key (usergroup, user)  
);

create table if not exists group_in_contest (
    usergroup integer not null,
    contest integer not null,
    foreign key(usergroup) references Usergroup(groupid),
    foreign key(contest) references Contest(contestcode),
    primary key (usergroup, contest)
);

create table if not exists contains_task (
    contest integer not null,
    task integer not null,
    foreign key(contest) references Contest(contestcode),
    foreign key(task) references Task(taskid),
    primary key (contest, task)
);

create table if not exists submits_task (
    user integer not null,
    task integer not null,
    verdict text not null,
    submission_time timestamp not null,
    foreign key(user) references User(userid),
    foreign key(task) references Task(taskid),
    primary key (user, task)
);
