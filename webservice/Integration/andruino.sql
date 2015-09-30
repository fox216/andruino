drop table if exists "devices";
drop table if exists "details";
drop table if exists "sessions";
drop table if exists "users";
drop table if exists "rules";
drop table if exists "statusreg";

CREATE TABLE "devices" (
"id" integer primary key autoincrement, 
"name" varchar(100) not null, 
"port" varchar(100) not null, 
"type" integer not null, 
"ts_added" datetime default current_timestamp, 
"ts_updated" datetime default current_timestamp, 
"enabled" integer not null, 
"submit" varchar(32) not null
);

CREATE TABLE "details" (
"id" integer primary key autoincrement, 
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
    "atime" NOT NULL default current_timestamp,
    "data" text
);

CREATE TABLE "users" (
"id" integer primary key autoincrement,
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

INSERT INTO "users" VALUES (NULL,"default","5f4dcc3b5aa765d61d8327deb882cf99","broken@email.addr");
INSERT INTO "users" VALUES (NULL,"matt","5f4dcc3b5aa765d61d8327deb882cf99","matt@email.addr");

