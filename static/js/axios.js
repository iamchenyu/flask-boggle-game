let score = 0;
let checkedWords = new Set();

const resultText = {
  ok: "Good job!",
  "not-on-board": "Sorry, we didn't find the word on the game board",
  "not-word": "hmm...we don't think it's a real word",
};

const timeOutFunc = async () => {
  current_score = $("#score").text();
  if (current_score) {
    //e.preventDefault();
    // AJAX doesn't navigate to a new page, it just returns the data to the script that made the request. if you're staying on the same page you can just use traditional AJAX to POST your data
    // `data` is the data to be sent as the request body
    // console.log("sending...");
    // await axios.post("/score", { data: { score: current_score } });
    // console.log("sent!");
    // The point of this snippet is to redirect the browser to a new URL specified by the action; if you're staying on the same page you can just use traditional AJAX to POST your data.
    post("/score", { score: current_score });
    alert("Time is Up!!!");
  }
};

/**
 * sends a request to the specified url from a form. this will change the window location.
 * @param {string} path the path to send the post request to
 * @param {object} params the parameters to add to the url
 * @param {string} [method=post] the method to use on the form
 * Source: https://stackoverflow.com/questions/133925/javascript-post-request-like-a-form-submit?page=1&tab=scoredesc#tab-top
 */

function post(path, params, method = "POST") {
  // The rest of this code assumes you are not using a library.
  // It can be made less verbose if you use one.
  const form = document.createElement("form");
  form.method = method;
  form.action = path;

  for (const key in params) {
    if (params.hasOwnProperty(key)) {
      const hiddenField = document.createElement("input");
      hiddenField.type = "hidden";
      hiddenField.name = key;
      hiddenField.value = params[key];

      form.appendChild(hiddenField);
    }
  }

  document.body.appendChild(form);
  form.submit();
}

$(window).on("load", () => {
  setTimeout(timeOutFunc, 60000);
});

const getWordResult = async (e) => {
  e.preventDefault();
  const word = $("#word").val().toLowerCase();
  // `params` are the URL parameters to be sent with the request
  // "/check?word=word"
  const res = await axios.get("/check", { params: { word: word } });
  const result = res.data.result;
  if (result == "ok") {
    if (!checkedWords.has(word)) {
      checkedWords.add(word);
      score = score + word.length;
      $("#score").text(score);
      $("<li>").text(word).appendTo($("#show-result"));
      $("#result").text(resultText[result]);
    } else {
      $("#result").text("This word already exists");
    }
  } else {
    $("#result").text(resultText[result]);
  }

  $("#word").val("");
};

$("#word-form").on("submit", getWordResult);
