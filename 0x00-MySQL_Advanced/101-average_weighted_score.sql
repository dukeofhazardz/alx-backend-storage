-- A SQL script that creates a stored procedure ComputeAverageWeightedScoreForUsers that computes and store the average weighted score for all students.

DROP PROCEDURE IF EXISTS ComputeAverageWeightedScoreForUsers;

DELIMITER $$
CREATE PROCEDURE ComputeAverageWeightedScoreForUsers()
BEGIN
    DECLARE user_id INT;

    DECLARE done INT DEFAULT 0;
    DECLARE cur CURSOR FOR SELECT id FROM users;
    DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = 1;

    OPEN cur;

    read_loop: LOOP
        FETCH cur INTO user_id;
        IF done THEN
            LEAVE read_loop;
        END IF;

        SET @total_score := (
            SELECT SUM(p.weight * c.score)
            FROM corrections c
            JOIN projects p ON c.project_id = p.id
            WHERE c.user_id = user_id
        );

        SET @total_weight := (
            SELECT SUM(p.weight)
            FROM corrections c
            JOIN projects p ON c.project_id = p.id
            WHERE c.user_id = user_id
        );

        IF @total_weight > 0 THEN
            SET @avg_weighted_score := @total_score / @total_weight;
        ELSE
            SET @avg_weighted_score := 0;
        END IF;

        UPDATE users
        SET average_score = @avg_weighted_score
        WHERE id = user_id;
    END LOOP;

    CLOSE cur;
END $$
DELIMITER ;
