CREATE TABLE "Company"(
    "CompanyName" VARCHAR(255) NOT NULL,
    "Address" VARCHAR(255) NOT NULL
);
CREATE TABLE "Person"(
    "PersonName" VARCHAR(255) NOT NULL,
    "PersonPhone" VARCHAR(255) NOT NULL,
    "PersonTitle" VARCHAR(255) NOT NULL
);
ALTER TABLE
    "Person" ADD PRIMARY KEY("PersonName");
CREATE TABLE "GeneralInformation"(
    "FileNumber" VARCHAR(255) NOT NULL,
    "PersonName" VARCHAR(255) NOT NULL,
    "CompanyName" VARCHAR(255) NOT NULL,
    "FileType" VARCHAR(255) NOT NULL,
    "FileName" VARCHAR(255) NOT NULL,
    "ReportDate" DATE NOT NULL,
    "Signature" VARCHAR(255) NOT NULL,
    "OtherManagers" VARCHAR(255) NOT NULL,
    "Description" VARCHAR(255) NOT NULL,
    "NumberOfOtherIncludedManagers" INTEGER NOT NULL,
    "InformationTableEntryTotal" INTEGER NOT NULL,
    "InformationTableValueTotal" INTEGER NOT NULL,
    "RerportType" VARCHAR(255) NOT NULL
);
ALTER TABLE
    "GeneralInformation" ADD PRIMARY KEY("FileNumber");
CREATE TABLE "InformationTable"(
    "FileNumber" VARCHAR(255) NOT NULL,
    "NameOfIssuer" VARCHAR(255) NOT NULL,
    "Class" VARCHAR(255) NOT NULL,
    "Cusip" VARCHAR(255) NOT NULL,
    "SharesValueInThousands" INTEGER NOT NULL,
    "SharesAmount" INTEGER NOT NULL,
    "InvestmentDiscretion" VARCHAR(255) NOT NULL,
    "OtherManagers" VARCHAR(255) NOT NULL,
    "VothingAuthoritySole" INTEGER NOT NULL,
    "VotingAuthorityShared" INTEGER NOT NULL,
    "VotingAuthorityNone" INTEGER NOT NULL
);
ALTER TABLE
    "InformationTable" ADD PRIMARY KEY("FileNumber");
ALTER TABLE
    "GeneralInformation" ADD CONSTRAINT "generalinformation_personname_foreign" FOREIGN KEY("PersonName") REFERENCES "Person"("PersonName");
ALTER TABLE
    "GeneralInformation" ADD CONSTRAINT "generalinformation_companyname_foreign" FOREIGN KEY("CompanyName") REFERENCES "Company"("CompanyName");
ALTER TABLE
    "InformationTable" ADD CONSTRAINT "informationtable_filenumber_foreign" FOREIGN KEY("FileNumber") REFERENCES "GeneralInformation"("FileNumber");