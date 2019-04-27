DELIMITER $$
CREATE procedure `decompose`  ()
BEGIN
	DECLARE business_id1 text ;
	DECLARE categories1 longtext;
	DECLARE done INT DEFAULT FALSE;
	DECLARE categoriesCursor CURSOR FOR
		select business_id, categories from business;
	DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = TRUE;
	OPEN categoriesCursor;
	myloop: LOOP
		FETCH Next from categoriesCursor into business_id1, categories1;
        IF done THEN
			close categoriesCursor;
			LEAVE myloop;
		END IF;
        CALL storeData(business_id1,categories1);
	END LOOP myloop;
END $$



DELIMITER $$
CREATE Procedure storeData(
  IN business_id1 text,
  IN categories1 longtext
)
BEGIN
	Declare categoriesCount int;
    Declare c1 int;
    Declare category text;
    Select length(categories1)-length(replace(categories1,',',''))+1 into categoriesCount;
    set c1 =1;
    myloop:Loop
		IF c1 > categoriesCount THEN
			LEAVE myloop;
		END IF;
		set category = SPLIT_STRING(categories1,',',c1);
		INSERT INTO `project2`.`business_category`(`business_id`,`category`) VALUES(business_id1,category);
		set c1 = c1+1;
	END Loop;
END $$

#DROP function `SPLIT_STRING`;
CREATE FUNCTION `SPLIT_STRING`(
	str text,
	delim VARCHAR(12),
	pos INT
) RETURNS text DETERMINISTIC RETURN REPLACE(
	SUBSTRING(
		SUBSTRING_INDEX(str , delim , pos) ,
		CHAR_LENGTH(
			SUBSTRING_INDEX(str , delim , pos - 1)
		) + 1
	) ,
	delim ,
	''
);

drop table business_category;
CREATE TABLE IF NOT EXISTS business_category(
business_id text,
category VARCHAR(255)
);

DELIMITER $$
CREATE procedure `get_distinct_businesses_count`  (OUT distinct_businesses_count INT)
BEGIN
	SELECT DISTINCT(COUNT(business_id)) INTO distinct_businesses_count from business;
END $$


DELIMITER $$
CREATE procedure `get_distinct_category_count`  (OUT distinct_category_count INT)
BEGIN
	SELECT DISTINCT(COUNT(category)) INTO distinct_category_count from business_category;
END $$


DELIMITER $$
CREATE procedure `get_top_10_categories_demo`()
BEGIN
  SELECT category from business_category group by category order by count(category) DESC LIMIT 10;
END $$


DELIMITER $$
CREATE procedure `get_filtered_users`(IN min_review_count INT)
BEGIN
  SELECT user_id from user where review_count > min_review_count;
END $$

DELIMITER $$
CREATE procedure `get_filtered_reviews`(IN star INT,IN category VARCHAR(100))
BEGIN
  SELECT user_id, business_id from review where stars = star and business_id in (SELECT business_id from business where categories like CONCAT('%',category,'%'));
END $$

DELIMITER $$
CREATE procedure `get_filtered_businesses`(IN category VARCHAR(100))
BEGIN
  SELECT business_id, categories from business where categories like CONCAT('%',category,'%');
END $$

DELIMITER $$
CREATE PROCEDURE `get_columns`(
IN db_name VARCHAR(255),
IN tab_name VARCHAR(255))
  BEGIN
	SELECT `COLUMN_NAME`
	FROM `INFORMATION_SCHEMA`.`COLUMNS`
	WHERE `TABLE_SCHEMA`=db_name
    AND `TABLE_NAME`=tab_name;
  END;$$

DELIMITER $$
CREATE PROCEDURE `get_data`(
IN tab_name VARCHAR(255))
  BEGIN
	SET @sql = CONCAT('SELECT * FROM ',tab_name,' limit 5');
	PREPARE stmt FROM @sql;
	EXECUTE stmt;
	DEALLOCATE PREPARE stmt;
  END;$$


DELIMITER $$
CREATE PROCEDURE `get_review_distribution`()
	BEGIN
	SELECT stars, count(stars) from review group by stars order by stars;
	END$$:

DELIMITER $$
CREATE PROCEDURE `get_businesses_with_highest_ratings`(IN count1 INT)
	BEGIN
			SELECT name, review_count from business order by review_count DESC LIMIT count1;
	END;$$

DELIMITER $$
CREATE PROCEDURE `get_business_categories_with_highest_ratings`(IN count1 INT)
	BEGIN
		SELECT category, count(*) as category_count from business_category group by category order by category_count DESC LIMIT count1;
	END;$$


DELIMITER $$
CREATE PROCEDURE `get_businesses_five_stars(`(IN count1 INT)
	BEGIN
	select business_id,count(*) as business_count from review where stars = 5.0 group by business_id order by business_count DESC limit count1;
	END;$$

DELIMITER $$
CREATE PROCEDURE `get_businesses_name_from_id(`(IN business_id VARCHAR(100))
	BEGIN
	select name from business where business_id = business_id;
END;$$
