-- Table: public.ctt_tickets

-- DROP TABLE IF EXISTS public.ctt_tickets;

CREATE TABLE IF NOT EXISTS public.ctt_tickets
(
    ticket_id uuid[] NOT NULL,
    "TowerID" character varying(100) COLLATE pg_catalog."default",
    "TowerLocation" character varying(100) COLLATE pg_catalog."default",
    "EquipmentID" character varying(100) COLLATE pg_catalog."default",
    "ErrorCode" character varying(100) COLLATE pg_catalog."default",
    "ErrorDetails" character varying(2000) COLLATE pg_catalog."default",
    "ErrordDateTime" timestamp with time zone,
    "AssignedUser_ID" character varying(30) COLLATE pg_catalog."default",
    "AssignedDateTime" timestamp with time zone,
    "Ticket_Status" character varying(30) COLLATE pg_catalog."default",
    "CompletedDateTime" timestamp with time zone,
    CONSTRAINT ctt_tickets_pkey PRIMARY KEY (ticket_id)
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.ctt_tickets
    OWNER to postgres;