ALTER TABLE `redesogcs`.`provincia` DROP PRIMARY KEY,
 ADD PRIMARY KEY  USING BTREE(`codigo`, `numpro`);
