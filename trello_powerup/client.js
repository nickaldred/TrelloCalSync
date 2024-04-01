var GRAY_ICON = 'https://cdn.hyperdev.com/us-east-1%3A3d31b21c-01a0-4da2-8827-4bc6e88b7618%2Ficon-gray.svg';

var addToCalendar= function (t, date) {
  console.log("Adding to calendar: " + date);
  
};

var btnCallback = function (t) {
    return t.popup({
        title: 'Pick a date and time',
        type: 'datetime',
        callback: function(t, opts) {
            return addToCalendar(t, opts.date);
        },
        date: Date,
      })};

window.TrelloPowerUp.initialize({
  'card-buttons': function (t, opts) {
    return [{
      icon: GRAY_ICON,
      text: 'Add to Calendar',
      callback: btnCallback
    }];
  }
});
