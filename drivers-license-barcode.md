# What's in the barcode on a driver's license

> The wide barcode on the back of a US or Canadian license is a PDF417 symbol laid out by AAMVA's DL/ID Card Design Standard. It holds the details printed on the front, such as name, birth date, expiry, license number, address and physical description, plus the issuer's six-digit Issuer Identification Number. Each field starts with a three-letter code, such as DBB for date of birth.

Source page: https://coderalert0.github.io/doorproof-site/drivers-license-barcode.html
Checked against its sources on November 7, 2026. Published by Doorproof, an ID scanner app for iPhone and iPad. Not legal advice.

## The standard behind it

AAMVA, the association of US and Canadian motor vehicle agencies, publishes the DL/ID Card Design Standard. Its Annex D sets out the PDF417 barcode that states and provinces print on the back of driver's licenses and ID cards. The standard is why one scanner can read a card from any state.

## How the barcode starts

The data opens with a header. It contains the characters `ANSI`, then the issuer's six-digit Issuer Identification Number (IIN), then the version of the standard the card follows. AAMVA assigns the IINs: 636014 is California, for example, and 636015 is Texas. A barcode whose IIN doesn't belong to the state printed on the front wasn't made by that state.

## The fields door staff care about

Each field is a three-letter element ID followed by its value.

| Code | Field | What it tells you |
|---|---|---|
| DBB | Date of birth | Age, counted to the day |
| DBA | Expiration date | Whether the card is still valid |
| DBD | Issue date | When this card was printed |
| DDJ | Under 21 until | The date the holder turns 21 |
| DDH | Under 18 until | The date the holder turns 18 |
| DDI | Under 19 until | The date the holder turns 19 |
| DCS | Family name | Last name |
| DAC | First name | First name |
| DAD | Middle name | Middle name or initial |
| DAQ | Customer ID number | The license or ID number |
| DAG, DAI, DAJ, DAK | Street, city, state, postal code | The address on the card |
| DBC | Sex | 1 male, 2 female, 9 not specified |
| DAU | Height | Height, to compare with the person |
| DAY | Eye color | Eye color, to compare with the person |

## Dates are written two ways

US cards write dates as month, day, year (MMDDCCYY). Canadian cards write them as year, month, day (CCYYMMDD). A reader that assumes one order misreads the other country's cards, so a good scanner checks which order makes sense for the issuer.

## Under-21 cards

The standard specifies a vertical card format for drivers under 21, optional in Canada. California and Virginia both print their under-21 cards vertically. A vertical card at a bar door deserves a careful look at the birth date and the under-21 date.

## What the barcode can prove, and what it can't

The fields have to agree with each other. The under-21 date must fall exactly 21 years after the birth date. The issue date must come before the expiry date. The IIN must match the issuing state. When they don't agree, the barcode was edited or built by hand.

When they do agree, the barcode only proves it was encoded correctly. Fake ID sellers encode correct barcodes too. See [do ID scanners detect fake IDs?](https://coderalert0.github.io/doorproof-site/do-id-scanners-detect-fake-ids.md)

## Frequently asked questions

### What type of barcode is on a driver's license?

A PDF417 barcode, a stacked two-dimensional barcode. AAMVA's card design standard defines what goes in it for US and Canadian licenses and ID cards.

### What does DDJ mean on a license barcode?

DDJ is the "Under 21 Until" field: the date the cardholder turns 21. It's written in the same date order as the card's other dates.

### Can a phone read a driver's license barcode?

Yes. Any phone camera can decode PDF417. An app then has to parse the AAMVA fields and check the dates and issuer.

### Does the barcode contain the photo?

No. The standard's barcode holds text fields, not the cardholder's photo, so staff still compare the face to the photo on the card.

## Sources

- [AAMVA DL/ID Card Design Standard (2025)](https://www.aamva.org/getmedia/81af105d-8b1b-45e1-aa46-f1800a259ed1/AAMVADLIDCardDesignStandard2025.pdf)
- [AAMVA: Issuer Identification Numbers (IIN)](https://www.aamva.org/identity/issuer-identification-numbers-(iin))
- [California ABC: Checking Identification](https://www.abc.ca.gov/education/licensee-education/checking-identification)
- [Virginia ABC: Detecting Fake IDs](https://www.abc.virginia.gov/licenses/retail-resources/preventing-underage-sales/detecting-fake-ids)
