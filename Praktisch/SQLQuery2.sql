USE FinancialReports;
GO

CREATE TABLE ReportFiles (
    FileNumber VARCHAR(255) PRIMARY KEY,
    FileType VARCHAR(50),
    Filename VARCHAR(255),
    Description VARCHAR(255),
    ReportDate DATE,
    CompanyName VARCHAR(255),
    PersonName VARCHAR(255),
    Title VARCHAR(100),
    Phone VARCHAR(50),
    Signature TEXT,
    ReportType VARCHAR(50),
    Address VARCHAR(255),
    NumberOfOtherIncludedManagers INT,
    InformationTableEntryTotal INT,
    InformationTableValueTotal VARCHAR(50),
    ListOfOtherIncludedManagers TEXT,
    InformationTable TEXT
);
GO
