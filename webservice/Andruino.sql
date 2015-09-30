drop table "devices";
drop table "details";
drop table "sessions";
drop table "users";
drop table "statusreg";


CREATE TABLE "devices" (
"id" integer not null primary key, 
"name" varchar(100) not null, 
"port" varchar(100) not null, 
"type" integer not null, 
"ts_added" datetime default current_timestamp, 
"ts_updated" datetime default current_timestamp, 
"enabled" integer not null, 
"submit" varchar(32) not null
);

CREATE TABLE "details" (
"id" integer not null primary key, 
"device_id" integer not null references "devices" ("id"), 
"label" varchar(100) not null, 
"ddr" integer not null, 
"pin" integer not null, 
"value" integer not null, 
"ts_value" datetime default current_timestamp, 
"last_value" integer not null, 
"ts_output" datetime default current_timestamp, 
"enabled" integer not null, 
"submit" varchar(32) not null
);

CREATE TABLE "sessions" (
    "session_id" char(128) UNIQUE NOT NULL,
    "atime timestamp" NOT NULL default current_timestamp,
    "data" text
);

CREATE TABLE "users" (
"id" interger not null primary key,
"username" varchar(32) not null,
"password" varchar(32) not null,
"email" varchar(64) not null
);

CREATE TABLE "statusreg" (
"device_id" integer not null references "devices" ("id"), 
"ts_value" datetime default current_timestamp
);



CREATE TABLE "rules" (
"device_id" integer not null references "devices" ("id"), 
"value" integer not null
);
