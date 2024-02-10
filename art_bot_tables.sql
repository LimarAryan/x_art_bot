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
