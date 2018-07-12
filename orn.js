var { URL } = require('./url.js')
var request = require('request')
var MongoClient = require('mongodb').MongoClient;
var urlDB = "mongodb://localhost:27017/";

getDateNow = () => {
  var today = new Date();
  var dd = today.getDate();
  var mm = today.getMonth() + 1;

  var yyyy = today.getFullYear();
  if (dd < 10) {
    dd = '0' + dd;
  }
  if (mm < 10) {
    mm = '0' + mm;
  }
  return yyyy + '-' + mm + '-' + dd
}

var fromDate = '2018-03-16'
var toDate = getDateNow()
var bnkName = 'bnk48official.orn'
var url = URL + fromDate + '/' + toDate + '/posts/column_chart'

request(url, function (error, response, body) {
  var ornToJSON = JSON.parse(body)
  var orn = ornToJSON.collectors['bnk48official.orn']
  orn.map((data) => {
    MongoClient.connect(urlDB, function (err, db) {
      if (err) throw err;
      var dbo = db.db("orn");
      var postID = data.pcid.split('_')
      var obj = [
        {
          _id: postID[1],
          url: 'http://facebook.com/' + data.pcid,
          info: {
            share_count: data.info.shares_count,
            comments_count: data.info.comments_count,
            reactions: {
              wow: data.info.reactions.wow,
              sad: data.info.reactions.sad,
              love: data.info.reactions.love,
              like: data.info.reactions.like,
              haha: data.info.reactions.haha,
              angry: data.info.reactions.angry,
            },
          },
          date: data.date
        }
      ]
      dbo.collection("ornly").insert(obj, function (err, res) {
        if (err) throw err;
        console.log('1 document insert :', postID[1])
        db.close();
      });
    });
  })
})
