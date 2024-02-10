-- Create table for published images
CREATE TABLE published_images (
    uuid VARCHAR(64) PRIMARY KEY,
    iiifurl VARCHAR(512),
    iiifThumbURL VARCHAR(512),
    viewtype VARCHAR(32),
    "sequence" VARCHAR(32),
    width INTEGER,
    height INTEGER,
    maxpixels INTEGER,
    created TIMESTAMP WITH TIME ZONE,
    modified TIMESTAMP WITH TIME ZONE,
    depictstmsobjectid INTEGER,
    assistivetext TEXT
);


--Add objects table to get title, artist, and year
CREATE TABLE object (
    objectid INTEGER PRIMARY KEY,
    accessioned INTEGER,
    accessionnum VARCHAR(32),
    locationid INTEGER,
    title VARCHAR(2048),
    displaydate VARCHAR(256),
    beginyear INTEGER,
    endyear INTEGER,
    visualbrowsertimespan VARCHAR(32),
    medium VARCHAR(2048),
    dimensions VARCHAR(2048),
    inscription VARCHAR,
    markings VARCHAR,
    attributioninverted VARCHAR(1024),
    attribution VARCHAR(1024),
    provenancetext VARCHAR,
    creditline VARCHAR(2048),
    classification VARCHAR(64),
    subclassification VARCHAR(32),
    visualbrowserclassification INTEGER,
    parentid INTEGER,
    isvirtual INTEGER,
    departmentabbr VARCHAR(32),
    portfolio VARCHAR(32),
    series VARCHAR(850),
    volume VARCHAR(850),
    watermarks VARCHAR(512),
    lastdetectedmodification TIMESTAMP WITH TIME ZONE,
    wikidataid VARCHAR(64),
    customprinturl VARCHAR(512)
);

