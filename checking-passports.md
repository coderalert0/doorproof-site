# How to check a passport at the door

> Check the photo page. Compare the photo, count the age from the birth date and make sure it hasn't expired. The two lines of letters and chevrons at the bottom are the machine-readable zone set by ICAO Doc 9303. They repeat the passport number, birth date and expiry, each followed by a check digit, so a date changed by hand usually breaks the math.

Source page: https://coderalert0.github.io/doorproof-site/checking-passports.html
Checked against its sources on November 7, 2026. Published by Doorproof, an ID scanner app for iPhone and iPad. Not legal advice.

## Is a passport acceptable ID?

Usually, but it depends on the state. California accepts US and foreign passports with a photograph, even though they carry no physical description. Virginia's list includes US passports. Check your state's rules and your venue's policy.

## The photo page

A passport carries the details on its data page: photo, name, nationality, date of birth, sex, issue and expiry dates, and the passport number. Check it the way you would a license. Do the math on the birth date, check the expiry and compare the face, focusing on the nose, chin, ears and eyes.

## The machine-readable zone

At the bottom of the data page are two lines of 44 characters each, using capital letters, digits and the `<` filler. ICAO Doc 9303, the international standard for travel documents, defines them.

- **Line 1:** `P`, the issuing country's three-letter code, then the surname and given names separated by `<<`.
- **Line 2:** the passport number and its check digit, the nationality, the birth date as YYMMDD and its check digit, the sex, the expiry date as YYMMDD and its check digit, an optional personal number and its check digit, and a final check digit over the number, the two dates and the personal number.

Many national ID cards use a three-line version of 30 characters each, with the same idea.

## Check digits catch edits

Each check digit comes from the field just before it. Every character gets a value: digits count as themselves, letters A to Z count as 10 to 35, and `<` counts as 0. The values are multiplied by 7, 3 and 1 in turn, added up, and the last digit of the sum is the check digit. Change one digit of a birth date and the check digit no longer matches. The final check digit covers the passport number, birth date, expiry and personal number together, each with its own check digit.

A matching check digit doesn't prove the passport is real. A forger can compute check digits too. It does mean the lines were encoded consistently, and a mismatch means something was changed.

## Two-digit years

The machine-readable zone writes years with two digits. A reader has to work out the century: a birth year of 05 is 2005, not 1905, for anyone standing at your door. The printed date on the page settles it.

## Frequently asked questions

### Can I scan a passport with a phone?

Yes. An app can read the two machine-readable lines with the camera, check the check digits, and count the age from the birth date.

### Do passports show an under-21 date?

No. Unlike many US licenses, a passport has no "under 21 until" date, so count the age from the birth date.

### Are foreign passports acceptable for alcohol?

California accepts foreign passports with a photograph. Other states differ, so check with your state's alcohol regulator.

## Sources

- [ICAO Doc 9303: Machine Readable Travel Documents](https://www.icao.int/publications/doc-series/doc-9303)
- [California ABC: Checking Identification](https://www.abc.ca.gov/education/licensee-education/checking-identification)
- [Virginia ABC: Detecting Fake IDs](https://www.abc.virginia.gov/licenses/retail-resources/preventing-underage-sales/detecting-fake-ids)
