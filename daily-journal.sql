   SELECT
            a.id,
            a.concept,
            a.entry,
            a.date,
            a.moodId
        FROM entries a
        WHERE a.entry LIKE "%"||?||"%"