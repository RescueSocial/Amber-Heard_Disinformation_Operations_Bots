function YoutubeScraper2() {
  var spreadsheet = SpreadsheetApp.getActiveSpreadsheet()
  var activeSheet = SpreadsheetApp.getActiveSheet()

  var q = "amber heard eve barlow"

  var search = YouTube.Search.list('snippet, id',{'q': q, maxResults: 100, pageToken:''})
  var results = search.items.map((item) => [item.id.videoId, item.snippet.title, item.snippet.description])
  var nextToken = search.nextPageToken
  console.log(nextToken)
  activeSheet.getRange(1, 1, results.length, results[2].length).setValues(results)

  var search = YouTube.Search.list('snippet, id', {'q': q, maxResults: 100, pageToken:'CDIQAA'})
  var results = search.items.map((item) => [item.id.videoId, item.snippet.title, item.snippet.description])
  var nextToken = search.nextPageToken
  console.log(nextToken)
  activeSheet.getRange(51, 1, results.length, results[2].length).setValues(results)

  var search = YouTube.Search.list('snippet, id', {'q': q, maxResults: 100, pageToken:'CGQQAA'})
  var results = search.items.map((item) => [item.id.videoId, item.snippet.title, item.snippet.description])
  var nextToken = search.nextPageToken
  console.log(nextToken)
  activeSheet.getRange(101, 1, results.length, results[2].length).setValues(results)

  var search = YouTube.Search.list('snippet, id', {'q': q, maxResults: 100, pageToken:'CJYBEAA'})
  var results = search.items.map((item) => [item.id.videoId, item.snippet.title, item.snippet.description])
  var nextToken = search.nextPageToken
  console.log(nextToken)
  activeSheet.getRange(151, 1, results.length, results[2].length).setValues(results)

  var search = YouTube.Search.list('snippet, id', {'q': q, maxResults: 100, pageToken:'CMgBEAA'})
  var results = search.items.map((item) => [item.id.videoId, item.snippet.title])
  var nextToken = search.nextPageToken
  console.log(nextToken)
  activeSheet.getRange(201, 1, results.length, results[2].length).setValues(results)

  var search = YouTube.Search.list('snippet, id', {'q': q, maxResults: 100, pageToken:'CPoBEAA'})
  var results = search.items.map((item) => [item.id.videoId, item.snippet.title, item.snippet.description])
  var nextToken = search.nextPageToken
  console.log(nextToken)
  activeSheet.getRange(251, 1, results.length, results[2].length).setValues(results)

  var search = YouTube.Search.list('snippet, id', {'q': q, maxResults: 100, pageToken:'CKwCEAA'})
  var results = search.items.map((item) => [item.id.videoId, item.snippet.title, item.snippet.description])
  var nextToken = search.nextPageToken
  console.log(nextToken)
  activeSheet.getRange(301, 1, results.length, results[2].length).setValues(results)     


  var search = YouTube.Search.list('snippet, id', {'q': q, maxResults: 100, pageToken:'CN4CEAA'})
  var results = search.items.map((item) => [item.id.videoId, item.snippet.title, item.snippet.description])
  var nextToken = search.nextPageToken
  console.log(nextToken)
  activeSheet.getRange(351, 1, results.length, results[2].length).setValues(results)

  var search = YouTube.Search.list('snippet, id', {'q': q, maxResults: 100, pageToken:'CJADEAA'})
  var results = search.items.map((item) => [item.id.videoId, item.snippet.title, item.snippet.description])
  var nextToken = search.nextPageToken
  console.log(nextToken)
  activeSheet.getRange(401, 1, results.length, results[2].length).setValues(results)

  var search = YouTube.Search.list('snippet, id', {'q': q, maxResults: 100, pageToken:'CMIDEAA'})
  var results = search.items.map((item) => [item.id.videoId, item.snippet.title, item.snippet.description])
  var nextToken = search.nextPageToken
  console.log(nextToken)
  activeSheet.getRange(451, 1, results.length, results[2].length).setValues(results)

  var search = YouTube.Search.list('snippet, id', {'q': q, maxResults: 100, pageToken:'CPQDEAA'})
  var results = search.items.map((item) => [item.id.videoId, item.snippet.title, item.snippet.description])
  var nextToken = search.nextPageToken
  console.log(nextToken)
  activeSheet.getRange(501, 1, results.length, results[2].length).setValues(results)


  var search = YouTube.Search.list('snippet, id', {'q': q, maxResults: 100, pageToken:'CKYEEAA'})
  var results = search.items.map((item) => [item.id.videoId, item.snippet.title, item.snippet.description])
  var nextToken = search.nextPageToken
  console.log(nextToken)
  activeSheet.getRange(551, 1, results.length, results[2].length).setValues(results)

  var search = YouTube.Search.list('snippet, id', {'q': q, maxResults: 100, pageToken:'CNgEEAA'})
  var results = search.items.map((item) => [item.id.videoId, item.snippet.title, item.snippet.description])
  var nextToken = search.nextPageToken
  console.log(nextToken)
  activeSheet.getRange(601, 1, results.length, results[2].length).setValues(results)

  var search = YouTube.Search.list('snippet, id', {'q': q, maxResults: 100, pageToken:'CIoFEAA '})
  var results = search.items.map((item) => [item.id.videoId, item.snippet.title, item.snippet.description])
  var nextToken = search.nextPageToken
  console.log(nextToken)
  activeSheet.getRange(651, 1, results.length, results[2].length).setValues(results)

  
  var search = YouTube.Search.list('snippet, id', {'q': q, maxResults: 100, pageToken:'CLwFEAA '})
  var results = search.items.map((item) => [item.id.videoId, item.snippet.title, item.snippet.description])
  var nextToken = search.nextPageToken
  console.log(nextToken)
  activeSheet.getRange(701, 1, results.length, results[2].length).setValues(results)
}

