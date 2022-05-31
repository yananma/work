

```sql 
SELECT COUNT(*) FROM `notice`.`xpost` WHERE `siteid` IN (2, 50998, 71809, 625400, 625751) AND `facetid` = '78' AND `include_t` >= '2022-05-30 00:00:00' AND `include_t` <= '2022-05-30 23:59:59'   
```

```sql
SELECT * FROM `notice`.`xpost` WHERE `siteid` IN (2, 12, 99, 50998, 53445, 71809, 625400, 625751) AND `facetid` = '78' AND `include_t` >= '2022-05-30 15:00:00' AND `include_t` <= '2022-05-30 16:00:00' AND `noise_rank` = '0' AND `status` IN (0,1) LIMIT 0,1000
```
