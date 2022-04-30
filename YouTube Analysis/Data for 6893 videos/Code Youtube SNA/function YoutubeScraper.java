function YoutubeScraper() {
  var spreadsheet = SpreadsheetApp.getActiveSpreadsheet()
  var activeSheet = SpreadsheetApp.getActiveSheet()

  
  var search = YouTube.Search.list('snippet, id', {'q': 'amber heard elon musk', maxResults: 100, pageToken:'CKwCEAA'})
  var results = search.items.map((item) => [item.id.videoId])
  var nextToken = search.nextPageToken
  console.log(nextToken)
activeSheet.getRange(1, 8, results.length, results[2].length).setValues(results)
}
