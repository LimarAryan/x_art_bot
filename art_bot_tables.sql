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
    attributioninverted --TODO: Add Variable Types
    attribution
    provenancetext
    creditline
    classification
    subclassification
    visualbrowserclassification
    parentid
    isvirtual
    departmentabbr
    portfolio
    series
    volume
    watermarks
    lastdetectedmodification
    wikidataid
    customprinturl
);