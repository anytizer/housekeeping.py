CREATE TABLE "configs"
(
    "config_name"  TEXT NOT NULL,
    "config_value" TEXT NOT NULL,
    "config_notes" TEXT,
    "show"         TEXT NOT NULL,
    PRIMARY KEY ("config_name")
);