import os

outfile = "quick_reset.sql"

if __name__ == "__main__" :
    schema_folder_path = "schemas\\"
    schemas = [
        "drop_schemas.sql",
        "user_info_schema.sql",
        "game_connections_schema.sql",
        "transactions_schema.sql"
    ]
    trigger_folder_path = "triggers_events_views\\"
    triggers = [
        "schema_triggers.sql",
        "schema_events.sql",
        "schema_views.sql"
    ]

    out = open(outfile, "w")

    for file in schemas :
        fp = open(schema_folder_path + file, "r")
        fp_lines = fp.readlines()
        for line in fp_lines :
            out.write(line)
        fp.close()
    
    for file in triggers :
        fp = open(trigger_folder_path + file, "r")
        fp_lines = fp.readlines()
        for line in fp_lines :
            out.write(line)
        fp.close()

    out.close()