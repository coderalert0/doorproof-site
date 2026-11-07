# Do ID scanners detect fake IDs?

> Some fakes, not all. A scanner reads the barcode on the back of the card, so it catches expired and under-age cards, barcodes that don't follow the standard, and altered cards whose barcode no longer matches the front. A well-made fake carries a correctly encoded barcode and scans clean, so the card still needs a check by hand.

Source page: https://coderalert0.github.io/doorproof-site/do-id-scanners-detect-fake-ids.html
Checked against its sources on November 7, 2026. Published by Doorproof, an ID scanner app for iPhone and iPad. Not legal advice.

## What a scanner actually reads

Every US and Canadian driver's license and state ID card carries a PDF417 barcode on the back, laid out by the AAMVA DL/ID Card Design Standard. It holds the same details printed on the front: name, date of birth, expiry date, license number, address and physical description, plus a six-digit number that identifies the state or province that issued it.

A scanner decodes that barcode and does the math. It doesn't see the card's holograms, ultraviolet ink, laser engraving or thickness. A phone camera can't check those. Some dedicated hardware scanners add ultraviolet and image checks.

## What a scan catches

- **Under-age and expired cards.** The scanner reads the birth date and expiry date and counts them in your time zone, so nobody has to do the math at a busy door.
- **Barcodes that break the standard.** A barcode with a missing header, an unknown issuer number, impossible dates or garbled fields is a sign the card wasn't made by a state.
- **Barcodes that disagree with themselves.** The standard puts the date someone turns 21 in its own field. If that date doesn't follow from the birth date, or the card's issue date comes after its expiry, the barcode was edited or built by hand.
- **Fronts that don't match the barcode.** An altered card often has a new birth date printed on the front while the barcode still holds the old one. Comparing the two catches it.
- **Cards seen before.** A record of tonight's scans catches a real card handed back out the door to a friend: a [passed-back ID](https://coderalert0.github.io/doorproof-site/passed-back-id.md).

## What a scan can't catch

- **A good counterfeit.** Fake ID sellers encode barcodes that follow the standard. If every field is plausible and consistent, the card scans clean.
- **A borrowed ID.** A real, unexpired card belonging to an older sibling or friend scans perfectly. Only the photo, the person's answers and their behavior give it away.
- **Physical tampering the barcode doesn't show.** A replaced photo or a re-laminated card can leave the barcode untouched.

That's why California's and Virginia's alcohol regulators both teach a hand check, Feel, Look, Ask, Give back, on top of any scan. See [how to check an ID at the door](https://coderalert0.github.io/doorproof-site/how-to-check-an-id.md).

## Signed IDs are different

Mobile driver's licenses and IDs in a phone's wallet are signed by the issuing state. AAMVA's mobile ID guidelines describe how a reader checks that signature, so a forged or edited mobile ID fails the check. On iPhone, businesses read Apple Wallet IDs through Apple's ID Verifier.

Plastic cards are moving the same way. In 2026 AAMVA asked its members for feedback on a standard way to add a cryptographic signature to the PDF417 barcode. Until states issue cards with signed barcodes, a plastic card's barcode can be copied or invented.

## How to use a scan result

1. **A clean scan means the barcode adds up.** Still compare the photo, and check the card by hand if anything feels off.
2. **A flagged scan tells you what to look at.** An expired or under-age result settles it. A mismatch means the card needs a closer look and a question only the real holder could answer.
3. **An unreadable barcode isn't proof of a fake.** Barcodes wear out and crack. Check the card by hand instead.

## Frequently asked questions

### Can a fake ID pass a scanner?

Yes. A fake with a correctly encoded barcode scans clean on any barcode scanner. Scanners catch mistakes in the barcode and cards that are expired or under age, not a well-made counterfeit.

### Do bars legally have to scan IDs?

Rules on scanning, and on keeping the data, differ by state, and some states limit what a business may keep from a scan. Check with your state's alcohol regulator.

### What does it mean if an ID won't scan?

The barcode may be worn, cracked or poorly printed, or the card may not be a US or Canadian license. Treat it as a card to check by hand, not as proof that it's fake.

### Are mobile IDs harder to fake than plastic cards?

Yes. A mobile ID is signed by the issuing state, and the reader checks that signature. A plastic card's barcode carries no signature today.

## Sources

- [AAMVA DL/ID Card Design Standard (2025)](https://www.aamva.org/getmedia/81af105d-8b1b-45e1-aa46-f1800a259ed1/AAMVADLIDCardDesignStandard2025.pdf)
- [AAMVA: feedback requested on digital key signatures in the card barcode](https://www.aamva.org/publications-news/aamva-news/aamva-card-design-standard-feedback-on-digital-key-signatures-requested)
- [AAMVA Mobile Driver's License Implementation Guidelines](https://www.aamva.org/getmedia/261ed16b-3f5c-4678-a2db-cc3016934234/MobileDLImplementationGuidelines-Version1-3.pdf)
- [California ABC: Checking Identification](https://www.abc.ca.gov/education/licensee-education/checking-identification)
- [Virginia ABC: Detecting Fake IDs](https://www.abc.virginia.gov/licenses/retail-resources/preventing-underage-sales/detecting-fake-ids)
- [Apple Developer: ID Verifier](https://developer.apple.com/wallet/id-verifier/)
