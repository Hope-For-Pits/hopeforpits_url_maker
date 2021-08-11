# Hope For Pits URL Maker

Little project for making prefilled adoption application urls so we can add to Google site and create QR codes for crates at adoption events.

## Usage

To use the url maker you'll need to use chrome developer tool, if you're running chrome you can open with F12.

Here's [a tutorial](https://developer.chrome.com/docs/devtools/open/) on chrome dev tools if you're curious.

Use chrome dev tools on [adoption application page](https://airtable.com/shrL8Ozj2HE2G8LEO) to retrieve the response from GetRowsMatchingName GET request and paste it here.

it will look something like this:

``` js
{"msg":"SUCCESS","data":{"rowResults":[{"id":"recAQBiyRQVOpUUai","createdTime":"2021-07-07T18:53:31.000Z","cellValuesByColumnId":{"fldk63tdzoGOMN8JR":"Brandon"}}...
```

Copy and paste the json from the above steps into the form or just use the make_urls python script to make urls and qr codes. The command line script isn't really up to date so you might have to make a few directories.

This app is hosted at [http://urlmaker.hopeforpits.com:8000/](http://urlmaker.hopeforpits.com:8000/)
