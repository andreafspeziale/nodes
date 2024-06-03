DROP TABLE IF EXISTS node_tree;
DROP TABLE IF EXISTS node_tree_names;

CREATE TABLE node_tree(
  idNode INTEGER not null primary key,
  level  INTEGER not null,
  iLeft  INTEGER not null,
  iRight INTEGER not null
);

CREATE TABLE node_tree_names(
  id INTEGER not null primary key,
  language VARCHAR not null,
  nodeName VARCHAR not null,
  node_tree_idNode INTEGER not null references node_tree
);
