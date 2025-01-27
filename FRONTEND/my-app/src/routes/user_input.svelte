<script>
  let {
    user_input_1,
    user_input_2,
    extract_video_info,
    fetchThenPlot,
    current_state,
    currentTime = $bindable(),
  } = $props();

  

  function is_valid(url){
  const regex = /^((?:https?:)?\/\/)?((?:www|m)\.)?((?:youtube(-nocookie)?\.com|youtu.be))(\/(?:[\w\-]+\?v=|embed\/|v\/)?)([\w\-]+)(\S+)?$/;
  const match = url.match(regex);

  return match? true : false;
}
</script>

<div class="user_input_form">
  <input
    id="video_input"
    type="url"
    bind:value={user_input_1["youtube_video_link"]}
    placeholder="Enter YouTube video link"
    size="50"
    required
  />
  <button
    class="btn-1"
    onclick= {extract_video_info}
    disabled={current_state === "loading video" || user_input_1['youtube_video_link']== "" || !is_valid(user_input_1['youtube_video_link'])}>Upload</button
  >
</div>
{#if current_state == "done loading video" || current_state == "loading colors" || current_state == "done loading colors"}
  <div class="user_input_form">
    <form>
      <input
        id="time"
        type="text"
        bind:value={currentTime}
        placeholder="Enter video timestamp"
        disabled
        size="10"
        required
      />
      <!-- <label for="time">Time (ms)</label><br> -->

      <input
        type="number"
        max="15"
        min="3"
        bind:value={user_input_2["number_of_dominant_colors"]}
        placeholder="Enter number of colors you want"
        size="3"
        required
        disabled={current_state === "loading colors"}
      />
      <button
        class="glow-on-hover"
        onclick={fetchThenPlot}
        disabled={current_state === "loading colors" ||
          user_input_2["number_of_dominant_colors"] < 3 ||
          user_input_2["number_of_dominant_colors"] > 15}>Analyze</button
      >
    </form>
  </div>
{/if}

<style>
  .user_input_form {
    width: 30vw;
    display: flex;
    align-items: center;
    justify-content: center;
    padding-bottom: 1vh;
  }
  button {
    margin-left: 0.5vw;
    height: 35px;
    border-color: white;
  }
  /* button:hover{
    scale: 1.05;
    cursor: pointer;
  } */
  input {
    height: 30px;
    text-align: center;
    border-color: white;
  }
  form{
    height: 100%;
    width: 100%;
    display: flex;
    align-items: center;
    justify-content: center;
  }
</style>
