async function fetchCovidJSON() {
  const response = await fetch(
    "https://disease.sh/v3/covid-19/historical/all?lastdays=all"
  );
  const world_data = await response.json();
  return world_data;
}
fetchCovidJSON().then((world_data) => {
  var cases = world_data.cases; // fetched movies
  console.log(cases);
  let temp_data_2020 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0];
  let data_2020 = [];
  let dates = Object.keys(cases);
  console.log(dates);
  for (let i = dates.length - 1; i >= 0; i--) {
    let date = dates[i];
    year = date.split("/")[2];
    month = date.split("/")[0];
    day = date.split("/")[1];
    if (year == 20) {
      if (day == 1 && month == 1) {
        console.log(cases[`${month}/${day}/${year}`]);
        temp_data_2020[0] += cases[`${month}/${day}/${year}`];
      } else if (day == 1) {
        let current_day = cases[`${month}/30/${year}`];
        let previous_day = cases[`${month - 1}/${i - 1}/${year}`];
        let calc = current_day - previous_day;
        temp_data_2020[month - 1] += calc;
      } else {
        let current_day = cases[`${month}/${day}/${year}`];
        let previous_day = cases[`${month}/${day - 1}/${year}`];
        let calc = current_day - previous_day;
        temp_data_2020[month - 1] += calc;
      }
    }
  }
  console.log(temp_data_2020);
  data_2020 = temp_data_2020.pop();

  var trace1 = {
    x: [
      "February",
      "March",
      "April",
      "May",
      "June",
      "July",
      "August",
      "September",
      "October",
      "November",
      "December",
    ],
    y: data_2020,
    name: "World",
    type: "bar",
  };

  var trace2 = {
    x: [
      "February",
      "March",
      "April",
      "May",
      "June",
      "July",
      "August",
      "September",
      "October",
      "November",
      "December",
    ],
    y: [12, 18, 29],
    name: "India",
    type: "bar",
  };

  var trace3 = {
    x: [
      "February",
      "March",
      "April",
      "May",
      "June",
      "July",
      "August",
      "September",
      "October",
      "November",
      "December",
    ],
    y: [12000000, 18, 29],
    name: "USA",
    type: "bar",
  };

  var data = [trace1, trace2, trace3];

  var layout = { barmode: "group" };

  Plotly.newPlot("myDiv", data, layout);
});
