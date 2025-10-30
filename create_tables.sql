create table items
(
    id int primary key,
    price double,
    name varchar(32),
    description varchar(200)
);

create table users
(
    username varchar(20) primary key,
    email varchar(100),
    birthdate date
);

create table transactions
(
    id int primary key,
    username varchar(20),
    time datetime,
    foreign key (username) references users(username)
);

create table transaction_items
(
    transaction_id int,
    item_id int,
    price double,
    quantity int,
    primary key (transaction_id, item_id),
    foreign key (item_id) references items(id),
    foreign key (transaction_id) references transactions(id)
);

create table cart_items
(
    username varchar(20),
    item_id int,
    quantity int,
    primary key (username, item_id),
    foreign key (username) references users(username),
    foreign key (item_id) references items(id)
);
