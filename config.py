"""
JDE AI Assistant — Client Configuration
=========================================

CURRENT MODE: Schema exploration (DISCOVERY) — deliberately kept on for
this deployment, not a leftover. Any table the database account can see
is queryable (still read-only, still row-capped, still timed-out) — this
is used to look up real table titles and real, correctly-prefixed column
names directly from JDE's own documentation of itself, instead of
guessing from general JDE conventions, which had repeatedly produced
wrong column names (e.g. assuming bare aliases like ITM/LTTR/AN8, when
this environment's real physical columns are prefixed, e.g. IMITM).

To lock this down to only the curated TABLES list below (e.g. before a
handoff where that's the intent), flip RESTRICT_TO_APPROVED_TABLES to
True — the RULES list automatically adjusts its wording to match
whichever mode is active, so there's no separate text to remember to
update.
"""

# ---------------------------------------------------------------------------
# Schema configuration
# ---------------------------------------------------------------------------

# Default schema for any table without an explicit override below.
SCHEMA_PREFIX_DEFAULT = "CRPDTA"

SCHEMA_OVERRIDES = {
    "F9860": "OL920",   # Object Librarian Master
    "F9202": "DD920",   # Data Dictionary Alias/Glossary
    "F98711": "PY920",  # Table Design
}

# ---------------------------------------------------------------------------
# Table access mode
# ---------------------------------------------------------------------------
# True  = STRICT mode. Only tables explicitly listed in TABLES below can be
#         queried, regardless of what the underlying database account can
#         see. This is the required setting for any client-facing
#         deployment — it's a second layer of defense so that even a
#         broadly-privileged database account (e.g. a schema owner) doesn't
#         translate into the assistant being able to query anything.
#
# False = DISCOVERY mode. Any table can be queried (still read-only,
#         still row-capped, still timed-out) as long as it's a real table
#         the database account can see. Useful during active exploration
#         when you're deliberately using F9860/F98711/F9202 to learn what
#         exists and what its real columns are, before curating a
#         reviewed TABLES list. Deliberately left on for this deployment —
#         read-only enforcement, the row cap, and the query timeout still
#         apply regardless; this only removes the table curation.
RESTRICT_TO_APPROVED_TABLES = False

# ---------------------------------------------------------------------------
# Tables
# ---------------------------------------------------------------------------

TABLES = [
    {
        "name": "F9860",
        "description": (
            "Object Librarian Master — catalog of every object in the JDE system "
            "(tables, applications, business functions, batch programs). Use this "
            "to look up the real title of a table, e.g. 'what does F4101 mean?'"
        ),
        "columns": [
            ("SIOBNM", "TEXT", "object name, e.g. 'F4101'"),
            ("SIMD", "TEXT", "description/title, e.g. 'Item Master'"),
            ("SIFUNO", "TEXT", "object type code — 'TBLE' = table, 'APPL' = application, 'BSFN' = business function, 'UBE' = batch program"),
        ],
        "notes": [
            "To list only tables, filter WHERE SIFUNO = 'TBLE'.",
        ],
    },
    {
        "name": "F98711",
        "description": (
            "Table Design — links a table to its real PHYSICAL columns and to the "
            "Data Dictionary item that defines each column's business meaning. "
            "IMPORTANT: TDSQLC is the actual physical column name to use in SQL "
            "against the real table — JDE prefixes physical columns with a "
            "2-3 letter table code (e.g. F4101's item number column is IMITM, "
            "not bare ITM). Never assume a bare data item alias is the real "
            "column name — always confirm via TDSQLC first."
        ),
        "columns": [
            ("TDOBNM", "TEXT", "table name, e.g. 'F4101'"),
            ("TDOBND", "TEXT", "Data Dictionary item ID for this column — join key to F9202.FRDTAI"),
            ("TDSQLC", "TEXT", "the REAL physical SQL column name (prefixed), e.g. 'IMITM' — this is what belongs in a SELECT statement, not the bare alias"),
            ("TDPSEQ", "INTEGER", "sequence number — column order within the table"),
        ],
    },
    {
        "name": "F9202",
        "description": (
            "Data Dictionary Alias/Glossary — the real business meaning of each "
            "Data Dictionary item (the alias, e.g. ITM), reused consistently "
            "across every table that uses it. Join F98711.TDOBND to "
            "F9202.FRDTAI to explain what a given physical column actually means."
        ),
        "columns": [
            ("FRDTAI", "TEXT", "Data Dictionary item ID — join key from F98711.TDOBND"),
            ("FRDSCR", "TEXT", "the real description text, e.g. 'Item Number'"),
            ("FRSYR", "TEXT", "language/system code — typically filter to blank for the default language"),
        ],
    },
    {
        "name": "F4101",
        "description": "Item Master",
        "columns": [
            ("IMITM", "TEXT", "Item Number (Short) — JDE's internal short item number, primary key. VERIFIED via F98711/F9202 against real data."),
            ("IMDSC1", "TEXT", "item description (line 1). VERIFIED."),
            ("IMUOM1", "TEXT", "primary/default unit of measure (e.g. EA, CS, LB). VERIFIED."),
            ("IMSTKT", "TEXT", "stocking type — classifies how the item is stocked/handled. VERIFIED."),
        ],
        "notes": [
            "Physical columns on this table are prefixed with 'IM' — confirmed via F98711.TDSQLC. "
            "F4101 has 209 columns total; only the ones needed for common questions are listed here. "
            "Ask the assistant to query F98711 for the full list if a question needs a column not here.",
        ],
    },
    {
        "name": "F4211",
        "description": "Sales Order Detail",
        "columns": [
            ("SDDOCO", "INTEGER", "sales order number. Confirmed present in real column list, prefix pattern verified."),
            ("SDAN8", "INTEGER", "customer number. Confirmed present."),
            ("SDITM", "TEXT", "item number, references F4101.IMITM. Confirmed present."),
            ("SDSOQS", "REAL", "quantity ordered. Confirmed present."),
            ("SDUPRC", "REAL", "unit price. Confirmed present."),
            ("SDDRQJ", "TEXT", "requested date (YYYY-MM-DD). Confirmed present."),
            ("SDLTTR", "TEXT", "line status code (UDC 40/AT). VERIFIED real meanings differ from initial assumption: '545' = Pick Confirmation (order still in-process/open), '620' = Sales Update (final billing/close step, NOT open), '980' = Canceled in Order Entry. Open orders are typically NOT at 620 — check UDC 40/AT for the full code list before assuming a status meaning."),
        ],
        "notes": [
            "Physical columns on this table are prefixed with 'SD' — confirmed via F98711.TDSQLC. "
            "F4211 has 268 columns total, including 20 user-defined status fields (SDSO01-SDSO20) "
            "for custom order-status tracking beyond the standard SDLTTR field.",
        ],
    },
]

# ---------------------------------------------------------------------------
# Example question/SQL pairs
# ---------------------------------------------------------------------------

EXAMPLES = [
    (
        "What is the real title of table F4101?",
        "SELECT SIMD FROM {F9860} WHERE SIOBNM = 'F4101' AND SIFUNO = 'TBLE';",
    ),
    (
        "List every real physical column on table F4101, in order.",
        "SELECT TDSQLC, TDPSEQ FROM {F98711} WHERE TDOBNM = 'F4101' ORDER BY TDPSEQ;",
    ),
    (
        "List every real physical column on table F4211, in order.",
        "SELECT TDSQLC, TDPSEQ FROM {F98711} WHERE TDOBNM = 'F4211' ORDER BY TDPSEQ;",
    ),
    (
        "What does the column IMITM on table F4101 actually mean?",
        "SELECT g.FRDSCR FROM {F98711} d JOIN {F9202} g ON TRIM(g.FRDTAI) = TRIM(d.TDOBND) WHERE d.TDOBNM = 'F4101' AND d.TDSQLC = 'IMITM';",
    ),
    (
        "List every column on table F4211 with its real description.",
        "SELECT d.TDSQLC, g.FRDSCR FROM {F98711} d JOIN {F9202} g ON TRIM(g.FRDTAI) = TRIM(d.TDOBND) WHERE d.TDOBNM = 'F4211' ORDER BY d.TDPSEQ;",
    ),
    (
        "What is item 10001?",
        "SELECT IMITM, IMDSC1, IMUOM1 FROM {F4101} WHERE IMITM = '10001';",
    ),
    (
        "Show open sales orders for customer 12345.",
        "SELECT SDDOCO, SDITM, SDSOQS, SDUPRC, SDDRQJ FROM {F4211} WHERE SDAN8 = 12345 AND SDLTTR = '620';",
    ),
]

# ---------------------------------------------------------------------------
# General rules given to the model alongside the schema.
#
# The two mode-dependent rules below are built from RESTRICT_TO_APPROVED_TABLES
# rather than hardcoded — so switching modes can never again leave the model
# with instructions that contradict what the server will actually allow.
# ---------------------------------------------------------------------------

_STRICT_MODE_RULE = (
    "STRICT MODE IS ON: only the tables listed above (F9860, F98711, F9202, "
    "F4101, F4211) can be queried for actual data, regardless of what the "
    "underlying database account can see. You may still use F9860/F98711/F9202 "
    "to look up the real title and real physical columns of a table NOT in "
    "this list, for informational purposes — but a query against that "
    "table's own data will be refused. If asked something that needs a "
    "table outside this list, say so plainly and note that it can be added "
    "to this configuration once verified, rather than attempting the query."
)

_DISCOVERY_MODE_RULE = (
    "DISCOVERY MODE IS ON: you are not limited to only the tables described "
    "above. If asked about a table not listed here, you can and should look "
    "it up yourself: (1) query F9860 (filter SIFUNO = 'TBLE') to confirm the "
    "table exists and get its real title, (2) query F98711 for that table's "
    "real physical column names (TDSQLC), (3) join to F9202 (with TRIM() on "
    "both sides) for what each column means, (4) then query the actual "
    "table using those real, verified column names. Never guess a bare data "
    "item alias as a column name — always confirm via F98711 first, the "
    "same way F4101 and F4211 were verified in this file."
)

_DISCOVERY_MODE_SCHEMA_LOOKUP_RULE = (
    "For a table not listed in this config, you don't know its schema by "
    "default — the current login (CRPDTA) is a schema owner, so unprefixed "
    "table names work fine for anything CRPDTA owns. If a query on a "
    "newly-discovered table fails with 'table or view does not exist', it "
    "may live in a different schema — you can check with: SELECT owner, "
    "table_name FROM all_tables WHERE table_name = '<name>'."
)

RULES = [
    "Only write single SELECT statements. Never INSERT/UPDATE/DELETE/DROP/ALTER/TRUNCATE/CREATE/MERGE.",
    'Do not invent results. If query_jde_database returns "No matching records were found", say so plainly.',
    "CONFIRMED PATTERN: this environment's physical columns are prefixed per table — F4101 uses "
    "'IM' (e.g. IMITM), F4211 uses 'SD' (e.g. SDAN8, SDLTTR). This was verified via F98711.TDSQLC "
    "against real data, not assumed. Any table added to this config in the future should have its "
    "columns verified the same way before being trusted — query F98711 for the real TDSQLC values, "
    "don't assume a bare data item alias is the physical column name.",
    "F98711/F9202 joins in this environment need TRIM() on both sides of the join condition — "
    "confirmed via testing, this environment's Data Dictionary fields have whitespace padding that "
    "breaks exact-match joins.",
    "If a query fails with an unexpected column/table error on a table NOT yet listed here with a "
    "'VERIFIED' note, say so plainly rather than guessing alternate names — query F98711 for that "
    "table's real columns instead of retrying variations blindly.",
    _STRICT_MODE_RULE if RESTRICT_TO_APPROVED_TABLES else _DISCOVERY_MODE_RULE,
    "JDE date columns (suffix J, e.g. SDDRQJ) are stored in Julian format CYYDDD: C = century digit "
    "(0 = 1900s, 1 = 2000s), YY = two-digit year within century, DDD = day of year (1-366). Example: "
    "119144 = century 1 (2000s) + year 19 (2019) + day 144 of that year = May 24, 2019. Decode these "
    "before presenting dates to the user rather than showing the raw Julian number, and say so if "
    "you're not confident about a specific value's conversion.",
    "STATUS CODES ARE NOT SAFE TO ASSUME: this environment already disproved one assumption today "
    "(F4211.SDLTTR = '620' was assumed to mean 'open', but UDC 40/AT confirms 620 actually means "
    "Sales Update / closed, while 545 means still in-process/open). Always check the relevant UDC "
    "table (F0005, filtered by the right DRSY/DRRT system+type code) before stating what a status "
    "code means, rather than relying on general JDE convention.",
]

if not RESTRICT_TO_APPROVED_TABLES:
    RULES.append(_DISCOVERY_MODE_SCHEMA_LOOKUP_RULE)

# ---------------------------------------------------------------------------
# Department-based table access (optional — omit entirely if this
# deployment doesn't need per-department separation). See the connector's
# earlier setup notes: keys are what you'll set as JDE_DEPARTMENT per
# deployment in clients.json; values are table-name prefixes.
# ---------------------------------------------------------------------------
# DEPARTMENT_TABLE_PREFIXES = {
#     "finance": ["F09", "F04", "F03B"],
#     "sales": ["F42", "F0101"],
# }

# Derived — don't edit these directly, they're built from TABLES above.
ALLOWED_TABLES = {t["name"] for t in TABLES}
TABLE_SCHEMAS = {
    t["name"]: SCHEMA_OVERRIDES.get(t["name"], SCHEMA_PREFIX_DEFAULT) for t in TABLES
}
