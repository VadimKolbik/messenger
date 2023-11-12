
chats_filter = '''
SELECT "chats_chat"."id",
        "chats_chat"."type_chat",
        COUNT("chats_message"."id") AS "c"
FROM "chats_chat"
    INNER JOIN "chats_chat_members"
    ON ("chats_chat"."id" = "chats_chat_members"."chat_id")
    LEFT OUTER JOIN "chats_message"
    ON ("chats_chat"."id" = "chats_message"."chat_id")
WHERE "chats_chat_members"."customuser_id" IN (1)
GROUP BY "chats_chat"."id",
          "chats_chat"."type_chat"
HAVING COUNT("chats_message"."id") > 0
ORDER BY "chats_message"."time_create" DESC
LIMIT 21
'''