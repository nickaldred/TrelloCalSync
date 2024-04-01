var GRAY_ICON = 'https://cdn.hyperdev.com/us-east-1%3A3d31b21c-01a0-4da2-8827-4bc6e88b7618%2Ficon-gray.svg';

var addToCalendar= function (t, date, duration) {
    console.log("Adding to calendar: " + date);
    console.log("Duration: " + duration);
};

var getDuration= function (t, date) {
  console.log("Adding to calendar: " + date);

    return t.popup({
        title: 'Choose duration',
        items: [{
        text: '1 hour',
        callback: function (t, opts) {
            return addToCalendar(t, date, 1);
        }}, 
        {
        text: '2 hours',
        callback: function (t, opts) { return addToCalendar(t, date, 2);},
        },
        {
        text: 'All day',
        callback: function (t, opts) { return addToCalendar(t, date, 24);}
        }]
    });
    };

var btnCallback = function (t) {
    calendar_event_details = t.popup({
        title: 'Pick a date and time',
        type: 'datetime',
        callback: function(t, opts) {
            return getDuration(t, opts.date);
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
