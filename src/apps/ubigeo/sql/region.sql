ALTER TABLE `redesogcs`.`region` DROP PRIMARY KEY,
 ADD PRIMARY KEY  USING BTREE(`codigo`, `numreg`);
