// This file contains the client-side code for the Trello Power-Up.

var GRAY_ICON =
  "https://cdn.hyperdev.com/us-east-1%3A3d31b21c-01a0-4da2-8827-4bc6e88b7618%2Ficon-gray.svg";

/**
 * Generates a JSON string representing the event details, including
 * fetching the cardId and boardId from Trello.
 * @param {Object} t - The Trello object.
 * @param {string} date - The start date of the event.
 * @param {number} duration - The duration of the event in minutes.
 * @returns {string} JSON string representing the event details
 */
function generateJSON(t, date, duration) {
  return t.card("id").then(function (card) {
    return t.board("id").then(function (board) {
      var eventDetails = {
        cardId: card.id,
        boardId: board.id,
        start_date: date,
        duration: duration,
      };
      return JSON.stringify(eventDetails);
    });
  });
}

/**
 * Adds an event to the calendar.
 * @param {Object} t - The Trello object.
 * @param {string} date - The start date of the event.
 * @param {number} duration - The duration of the event in minutes.
 */
var addToCalendar = function (t, date, duration) {
  console.log("Adding to calendar: " + date);
  console.log("Duration: " + duration);

  // Get the JSON string directly from the generateJSON function
  generateJSON(t, date, duration).then((jsonString) => {
    console.log("JSON Event details: " + jsonString);

    fetch("url_here", {
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
};

/**
 * Retrieves the duration for a given date.
 *
 * @param {Object} t - The Trello object.
 * @param {Date} date - The date for which to retrieve the duration.
 * @returns {Promise} - A promise that resolves to the selected duration.
 */
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

/**
 * Callback function for the button click event.
 *
 * @param {Object} t - The Trello object.
 */
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
