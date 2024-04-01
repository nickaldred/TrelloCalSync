var GRAY_ICON =
  "https://cdn.hyperdev.com/us-east-1%3A3d31b21c-01a0-4da2-8827-4bc6e88b7618%2Ficon-gray.svg";

var addToCalendar = function (t, date, duration) {
  console.log("Adding to calendar: " + date);
  console.log("Duration: " + duration);

  t.card("id").then(function (card) {
    t.board("id").then(function (board) {
      var eventDetails = {
        cardId: card.id,
        boardId: board.id,
        start_date: date,
        duration: duration,
      };
      var jsonString = JSON.stringify(eventDetails);
      console.log("JSON Event details: " + jsonString);

      fetch("urlasdsdadsadasdasdsad", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: jsonString,
      })
        .then((response) => response.json())
        .then((data) => console.log("Success:", data))
        .catch((error) => console.error("Error:", error));
    });
  });
};

var getDuration = function (t, date) {
  console.log("Getting duration for: " + date);

  return t.popup({
    title: "Choose duration",
    items: [
      {
        text: "1 hour",
        callback: function (t, opts) {
          return addToCalendar(t, date, 1);
        },
      },
      {
        text: "2 hours",
        callback: function (t, opts) {
          return addToCalendar(t, date, 2);
        },
      },
      {
        text: "All day",
        callback: function (t, opts) {
          return addToCalendar(t, date, 24);
        },
      },
    ],
  });
};

var btnCallback = function (t) {
  calendar_event_details = t.popup({
    title: "Pick a date and time",
    type: "datetime",
    callback: function (t, opts) {
      return getDuration(t, opts.date);
    },
    date: Date,
  });
};

window.TrelloPowerUp.initialize({
  "card-buttons": function (t, opts) {
    return [
      {
        icon: GRAY_ICON,
        text: "Add to Calendar",
        callback: btnCallback,
      },
    ];
  },
});
