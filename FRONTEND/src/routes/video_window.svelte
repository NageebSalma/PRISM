<script>
  import { onMount , onDestroy} from "svelte";

  let { title, url, currentTime = $bindable(), current_state } = $props();

  let player;
  let videoId;
  let timeTrackingInterval 


  function getYouTubeVideoId(url) {
    const regex = /^((?:https?:)?\/\/)?((?:www|m)\.)?((?:youtube(-nocookie)?\.com|youtu.be))(\/(?:[\w\-]+\?v=|embed\/|v\/)?)([\w\-]+)(\S+)?$/;    
    const match = url.match(regex);

    return match[6] // Return the video ID or null if not found
  }

  function startTrackingTime() {
        clearInterval(timeTrackingInterval)
        timeTrackingInterval = 0;


    timeTrackingInterval = setInterval(() => {
      if (player && player.getCurrentTime) {
        currentTime = Math.floor(player.getCurrentTime() * 1000); // Get time in milliseconds
      }

    }, 1); // Update every millisecond
  }


  function initializePlayer() {
    console.log("this is url: ", url);

    videoId = getYouTubeVideoId(url);
    if (!videoId) {
      return 'Video Id Doesnt Exists'; // Avoid creating a player if the URL is invalid
    }

    if (player) {
      clearInterval(timeTrackingInterval);
      timeTrackingInterval = 0;

      player.destroy(); // Destroy the old player instance
      player = null;
      console.log("Destroyed Old Player Sucessfully");
    }

    let iframeElement = document.getElementById("player");
    if (!iframeElement) {
      console.error("Player element not found in the DOM.");
      return;
    }
    clearInterval(timeTrackingInterval);
    timeTrackingInterval = 0;


    player = new YT.Player("player", {
      videoId: videoId,
      playerVars: {
        controls: 1,
        modestbranding: 1,
        rel: 0,
        fs: 0,
      },
      events: {
        onReady: startTrackingTime,
        onStateChange: clearInterval(timeTrackingInterval)
      },
    });
  }

  function loadYouTubeAPI() {
    return new Promise((resolve) => {
      if (window.YT && YT.Player) {
        player = null;
        resolve(); // API is already loaded
      } else {
        const script = document.createElement("script");
        script.src = "https://www.youtube.com/iframe_api";
        script.onload = () => {
          window.onYouTubeIframeAPIReady = resolve; // Resolve when API is ready
        };
        document.body.appendChild(script);
      }
    });
  }

  onMount(async () => {
    console.log("Mounting the Video Window");
    await loadYouTubeAPI(); // Ensure API is loaded before initializing the player
    clearInterval(timeTrackingInterval);
    timeTrackingInterval = 0;
    initializePlayer(); // Reinitialize the player on URL change

  });


  onDestroy(() => {
    if (timeTrackingInterval) {
      clearInterval(timeTrackingInterval);
      timeTrackingInterval = 0;

    }

  })
</script>

<!-- 1. The <iframe> (and video player) will replace this <div> tag. -->
<div id="player">
  <iframe
    {title}
    frameborder="0"
    allow="accelerometer; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
  ></iframe>
</div>

<style>
  #player {
    margin-top: 2vh;
    display: flex;
    align-items: center;
    flex-direction: column;
    height:70vh;
    width: 80vw;
  }
  iframe {
    height: 100%;
    width: 100%;
  }
</style>
