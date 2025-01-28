<!-- svelte-ignore non_reactive_update -->
<!-- svelte-ignore non_reactive_update -->
<!-- TO RUN THIS UI =>  npm run dev -->

<script>
  import UserInput from "./user_input.svelte";
  import Video from "./video_window.svelte";
  let currentTime = $state(0);

  let vid_result = $state({});
  let result = $state({});
  let plotDiv = $state(null);
  let plot = $state(null);
  let url = "";
  let states = [
    "new",
    "loading video",
    "done loading video",
    "loading colors",
    "done loading colors",
  ];
  let current_state = $state(states[0]);

  let user_input_1 = $state({
    youtube_video_link: "",
  });
  let user_input_2 = $state({
    streaming_link: url,
    timestamp: "0",
    number_of_dominant_colors: 3,
  });

  function get_x_values(k, width) {
    let x_values = [0];
    for (let i = 1; i < k; i++) {
      x_values.push(x_values[i - 1] + width + 0.25);
    }
    return x_values;
  }

  function get_y_values(k, height) {
    let y_values = [];
    for (let i = 0; i < k; i++) {
      y_values.push(height);
    }
    return y_values;
  }

  function get_width_values(k, width) {
    let w_values = [];
    for (let i = 0; i < k; i++) {
      w_values.push(width);
    }
    return w_values;
  }

  async function extract_video_info() {
    try {
      user_input_2 = {
        streaming_link: url,
        timestamp: "0",
        number_of_dominant_colors: 3,
      };
      current_state = states[1];
      const vid_response = await fetch("http://localhost:8001/video", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(user_input_1),
      });
      vid_result = await vid_response.json();
    } catch (error) {
      console.error("Error:", error);
    } finally {
      current_state = states[2];
      url = vid_result["streaming_link"];
      user_input_2.streaming_link = url;
    }
  }

  async function fetchThenPlot() {
    try {
      user_input_2.timestamp = currentTime + "";
      current_state = states[3];
      const response = await fetch("http://localhost:8001/colors", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(user_input_2),
      });
      result = await response.json();
    } catch (error) {
      console.error("Error!!:", error);
    } finally {
      current_state = states[4]; // Update loading state

      let width = 5;
      let k = user_input_2["number_of_dominant_colors"];
      let height = 5;

      setTimeout(() => {
        let trace1 = {
          x: get_x_values(k, width),
          y: get_y_values(k, height),
          width: get_width_values(k, width),
          text: rgbs_to_hex(result["colors"]), // Custom hover text
          hoverinfo: "text", // Show only the text on hover
          marker: {
            color: rgbs_to_hex(result["colors"]),
          },
          type: "bar",
        };
        let layout = {
            paper_bgcolor: "rgba(0,0,0,0)",
            plot_bgcolor: "rgba(0,0,0,0)",
            dragMode: false,
            scrollZoom: false,
            xaxis: {
              visible: false,
              showgrid: false,
              fixedrange: true,
            },
            yaxis: {
              showgrid: false,
              visible: false,
              fixedrange: true,
            },
            showticklabels: false,
            margin: {
              l: 0,
              r: 0,
              b: 0,
              t: 0,
            },
          },
          plotDiv = document.getElementById("chartcontainer");
        // console.log("this is plotDiv ", plotDiv);
        plot = Plotly.newPlot(plotDiv, [trace1], layout, {
          displayModeBar: false,
        });

        plotDiv.on("plotly_click", function (eventData) {
          const color = eventData.points[0].text; // Value

          // Value to copy (customize as needed)
          const valueToCopy = `${color}`;

          // Copy to clipboard
          navigator.clipboard.writeText(valueToCopy);
        });
      }, 1);

    
    }
  }
  function rgbs_to_hex(array_of_rgbs) {
    let hex_values = [];
    array_of_rgbs.forEach((rgb_array) => {
      let [r, g, b] = rgb_array;
      let red = Math.round(r).toString(16).padStart(2, "0"); // FF
      let green = Math.round(g).toString(16).padStart(2, "0"); // C0
      let blue = Math.round(b).toString(16).padStart(2, "0"); // CB
      let hex_string = "#" + red + green + blue;
      hex_values.push(hex_string);
    });
    return hex_values;
  }
</script>

<main>
  <div class="home_page">
    <div class="title-input">
      <h1 id="title">PRISM</h1>
      <UserInput
        {user_input_1}
        {user_input_2}
        {fetchThenPlot}
        {extract_video_info}
        {current_state}
        {currentTime}
      />
      <!-- <input type="text" value={current_state} /> -->
    </div>

    {#if current_state == states[0]}
      <div id="starting-div">
        <h2>Hey There &hearts;</h2>
        <h2>Please enter a youtube video URL to continue!</h2>
      </div>
    {:else if current_state == states[1]}
      <div class="empty-video-window">
        <h2>Loading your video!</h2>
      </div>
    {:else if current_state == states[2] || current_state == states[3] || current_state == states[4]}
      <Video
        url={user_input_1["youtube_video_link"]}
        title={vid_result["title"]}
        bind:currentTime
        {current_state}
      />
      {#if current_state == states[2]}
        <div class="empty-colors-bar">
          <h3>1- Slide To Desired Frame</h3>
          <h3>2- Pick Number Of Dominant Colors</h3>
          <h3>3- Press Analyze</h3>
        </div>
      {/if}
    {/if}
    {#if current_state == states[3]}
      <div class="empty-colors-bar">
        <h2>Please wait as analysis is taking place ...</h2>
      </div>
    {:else if current_state == states[4]}
      <div id="chartcontainer" bind:this={plotDiv}></div>
    {/if}
  </div>
</main>

<!-- <Footer /> -->

<style>
  #title {
    /* padding-top: 1vh; */
    padding-bottom: 2vh;
    text-align: center;
    font-family: sans-serif;
    font-size: 3rem;
    letter-spacing: 0.15rem;
    text-transform: uppercase;
    color: #fff;
    text-shadow:
      -4px 4px #ef3550,
      -8px 8px #f48fb1,
      -12px 12px #7e57c2,
      -16px 16px #2196f3,
      -20px 20px #26c6da,
      -24px 24px #43a047,
      -28px 28px #eeff41,
      -32px 32px #f9a825,
      -36px 36px #ff5722;
  }

  .home_page {
    text-transform: uppercase;
    font-family: Monospace, sans-serif;

    display: flex;
    align-items: center;
    justify-content: center;
    flex-direction: column;
    color: white;
  }
  #starting-div {
    display: flex;
    align-items: center;
    justify-content: center;
    flex-direction: column;
    height: 60vh;
    width: 40vw;
    text-align: center;
    color: rgb(47, 130, 232);
    text-shadow: 2px 2px 2px rgb(47, 47, 47);
  }
  #starting-div h2:hover {
    color: rgb(232, 47, 164);
    text-shadow: 2px 2px 2px rgb(47, 47, 47);
  }
  .empty-video-window {
    margin-top: 8vh;
    display: flex;
    align-items: center;
    justify-content: center;
    flex-direction: column;
    color: rgb(246, 245, 245);
    height: 70vh;
    width: 80vw;
    border-color: #ffffff;
    background-color: rgb(212, 212, 212);
  }

  .empty-colors-bar {
    margin-top: 2vh;
    margin-bottom: 5vh;

    display: flex;
    align-items: center;
    justify-content: center;
    flex-direction: column;
    height: 25vh;
    width: 80vw;
    color: rgb(246, 245, 245);
    border-color: #ffffff;
    background-color: rgb(212, 212, 212);
    text-align: center;
  }
  #chartcontainer {
    /* margin-top: 2vh; */
    margin-bottom: 5vh;
    /* margin-bottom: 10vh; */
    height: 25vh;
    width: 80vw;
    display: flex;
    justify-content: center;
    overflow: auto;
    overflow-y: hidden;
  }
  main {
    height: 100%;
    width: 100%;
    margin: 0;
    padding: 0;
    padding-bottom: 8vh;
  }
</style>
