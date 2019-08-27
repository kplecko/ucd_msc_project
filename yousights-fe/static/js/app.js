let map;
let lat;
let lng;

let videoResponse;
let eventsResponse;
// Fetching the value of the text box and accordingly passing
// that to the payload to fetch live results from youtube
const noOfLiveVideos = 10;
const noOfCacheVideos = 50;

function loadJson(url, payload) {
  // load jason from API url
  // fetch data from the API
  return fetch(url, {
    credentials: 'same-origin',
    method: 'POST',
    body: JSON.stringify(payload),
    headers: new Headers({
      'Content-Type': 'application/json',
      // eslint-disable-next-line quote-props
      'Authorization': 'xxxxxxxxxxxxxxx',
    }),
  })
    .then(response => response.json())
    .catch(err => console.log(err, url));
}

function getData(url, payload) {
  // create promise for API load json
  // eslint-disable-next-line no-unused-vars
  const promise = new Promise((resolve, reject) => {
    const response = loadJson(url, payload);  
    // eslint-disable-next-line valid-typeof
    if (typeof response !== 'Object' && response !== null && response !== 'undefined') {
        resolve(response);
    } else {
      resolve({ 'status': 'error' });
    }
  });
  return promise;
}

// This function will sort the data based on the similarity value in Descending
function sortDesc(apiMockupData) {
  const videos = apiMockupData.video_statistic_data;
  videos.sort(function (a, b) {
    return a.data.en_transcript.trans_similarity > b.data.en_transcript.trans_similarity ? 1 : -1;
  });
  return videos;
}

// This function will sort the data based on the similarity value in Ascending
function sortAsc(apiMockupData) {
  const videos = apiMockupData.video_statistic_data;
  videos.sort(function (a, b) {
    return a.data.en_transcript.trans_similarity < b.data.en_transcript.trans_similarity ? 1 : -1;
  });
  return videos;
}

// This funstion will help in rank ordering the video based on the viewcount 
function rankOrderSort(apiMockupData) {
  const videos = apiMockupData.video_statistic_data;
  videos.sort(function (a, b) {
    return a.data.viewCount < b.data.viewCount ? 1 : -1;
  });
  return videos;
}

// This will help us in trimming the text and show ... in the comments displayed
function smartTrim(str, length, delim, appendix) {
  if (str.length <= length) return str;
  var trimmedStr = str.substr(0, length+delim.length);
  var lastDelimIndex = trimmedStr.lastIndexOf(delim);
  if (lastDelimIndex >= 0) trimmedStr = trimmedStr.substr(0, lastDelimIndex);
  if (trimmedStr) trimmedStr += appendix;
  return trimmedStr;
}

// This is the main method which will use the JSON data parse it and add it to the HTML
function resultsGenerator(chosenLanguage, apiMockupData, sortOrder) {
  // Calling the descending sort button to sort the videos
  if (sortOrder === 'desc') {
    videos = sortDesc(apiMockupData);
  // Calling the ascending sort button to sort the videos
  } else if (sortOrder === 'asc') {
    videos = sortAsc(apiMockupData);
  }else if (sortOrder === 'rankOrder') {
    videos = rankOrderSort(apiMockupData);
  } else {
    // this is the default sort order (as sent from the BE)
    videos = apiMockupData.video_statistic_data;
  }
  // Iterate over the JSON returned and display the details on the UI
  if (videos.length != 0 && videos != null) {
    for (let video = 0; video < videos.length; video++) {
      const title = videos[video].video_id;
      const similarity = videos[video].data.en_transcript.trans_similarity_nor;
      const likeCountVal = videos[video].data.likeCount;
      const dislikeCountVal = videos[video].data.dislikeCount;
      const titleVal = videos[video].data.title;
      const sumLikeDislike = likeCountVal + dislikeCountVal;
      const likeRatio = Math.round((likeCountVal / sumLikeDislike) * 100);
      const bestComments = videos[video].data.comments.sentiment.best_comments;
      const worstComments = videos[video].data.comments.sentiment.worst_comments;
      // create video ID for word cloud div
      const vidId = `wordCloud${video}`;
      
      // get list of words and create array for word cloud
      const wordCloudVal = videos[video].data.en_transcript.freq_trans;

      // Extracting the entities
      const entities = videos[video].data.en_transcript.entities;

      // Variable created to hold the details of the comments (it is in the more details button)
      let tableCreation ="";

       // Variable created to hold the details of the entities (it is in the more details button)
      let entityCreation = "";

      const resultsHtml = ` <div id="mainId" class="row border">
      <div class="row col-sm-12">
      <h6 class="col-sm-4 mt-2 card-title ml-3"><b>${titleVal}</b></h6>
      <h6 class="col-sm-6 mt-2 card-title ml-3 text-center"><b>KEYWORDS</b></h6>
          <div class="col-sm-4 center-block">
            <a href="#"
            data-toggle="modal"
            data-target="#${title}open">
            <img class="ml-3 imgStyle" id="iframeId" src="https://img.youtube.com/vi/${title}/0.jpg" style="width: 300px; 
            height: 280px; border: 0;" seamless=""></img>
            </a>
          </div>
         <div class="col-sm-6 center-block" id="${vidId}"></div>
            <div class="center-block col-sm-2">
                <div>
                  <div class="ml-5 mt-5 c100 p${likeRatio} small">
                    <span>${likeRatio}%</span>
                      <div class="slice">
                        <div class="bar"></div>
                        <div class="fill"></div>
                      </div>
                  </div>
                  <div class="myDiv">
                    <h6 class="relevance">Relevance</h6>
                    <div class="ml-5 mt-5 c100 p80 small">
                      <span>${similarity}</span>
                          <div class="slice">
                            <div class="bar"></div>
                            <div class="fill"></div>
                          </div>
                    </div>
                  </div>
                  <h6 class="likes">Likes</h6>
                  </div>
              </div>
          </div>
          <div id="moreInfoDiv" class="col-sm-12 ml-4">
            <p>
              <button class="col-sm-3 btn btn-info btn-lg btn-block text-center" type="button" data-toggle="collapse" data-target="#collapseExample${video}" aria-expanded="false" aria-controls="collapseExample">
                more details
              </button>
            </p>
            <div class="col-sm-12 collapse" id="collapseExample${video}">
              <div class="card card-body">
                <div id="collapseId${video}"></div>
                <span id="mySim${video}"></span>
              </div>
            </div>
            </div>
            </div>
          <div
      class="modal fade"
      id="${title}open"
      tabindex="-1"
      role="dialog"
      aria-labelledby="exampleModalLabel"
      aria-hidden="true"
      data-keyboard="false" 
      data-backdrop="static">
      <div class="modal-xl modal-dialog" role="document">
        <div class="modal-content">
          <div class="modal-header">
            <h2 class="modal-title" id="exampleModalLabel">
            ${titleVal}
            </h2>
            <button
              id="${title}close"
              type="button"
              class="close"
              data-dismiss="modal"
              aria-label="Close">
              <span>&times;</span>
            </button>
          </div>
          <div class="modal-body">
            <div class="container">
              <div class="row">
                <div class="col-xs-8 mr-4">
                  <iframe
                    id="${title}video"
                    width="800"
                    height="480"
                    src="https://www.youtube.com/embed/${title}">
                  </iframe>
                </div>
                <div class="col-xs-4">
                  <div>
                    <h3>Table Of Contents</h3>
                  </div>
                  <br/>
                  <ul>
                  <li id="${title}105"><span><a href="#">(1:45)</a>  : Installing Python & PyCharm</span></li>
                  <li id="${title}2906"><span id="time"><a href="#">(48:26)</a> : Getting Input From Users</span></li>
                  <li id="${title}5055"><span id="time"><a href="#">(1:24:15)</a> : Functions</span></li>
                  <li id="${title}8421"><span id="time"><a href="#">(2:20:21)</a> : Building a Guessing Game</span></li>
                  <li id="${title}11057"><span id="time"><a href="#">(3:04:17)</a> : Try / Except</span></li>        
                  </ul>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
    <script>
      $(function() {
        $("#${title}close").on("click", function setURL() {
          document.getElementById("${title}video").src =
            "https://www.youtube.com/embed/${title}";
        });
      });
      $(function() {
        $("#${title}105").on("click", function setURL() {
          document.getElementById("${title}video").src =
            "https://www.youtube.com/embed/${title}?enablejsapi=1&start=105&autoplay=1";
        });
      });
      $(function() {
        $("#${title}2906").on("click", function setURL() {
          document.getElementById("${title}video").src =
            "https://www.youtube.com/embed/${title}?enablejsapi=1&start=2906&autoplay=1";
        });
      });
      $(function() {
        $("#${title}5055").on("click", function setURL() {
          document.getElementById("${title}video").src =
            "https://www.youtube.com/embed/${title}?enablejsapi=1&start=5055&autoplay=1";
        });
      });
      $(function() {
        $("#${title}8421").on("click", function setURL() {
          document.getElementById("${title}video").src =
            "https://www.youtube.com/embed/${title}?enablejsapi=1&start=8421&autoplay=1";
        });
      });
      $(function() {
        $("#${title}11057").on("click", function setURL() {
          document.getElementById("${title}video").src =
            "https://www.youtube.com/embed/${title}?enablejsapi=1&start=11057&autoplay=1";
        });
      });
    </script>
  `;
      $('#content').find('#pills-tabContent').find('#pills-video').find('#container')
        .remove('#card');
      // Appending the data onto the Html result div inside the video tab
      $('#content').find('#pills-tabContent').find('#pills-video').find('#container')
        .find('#card')
        .append(resultsHtml);
        
      enableButtons();
      $('#loadContent').hideLoading();
      $('div#mainMenu').find('#feedback').css('display','inline');
      // Fetch the description and display when more button is clicked
      if (bestComments != null && bestComments.length !=0) {
      tableCreation += '<table class="table table-borderless table-sm table-hover"><thead><tr><th class="table-success"><p><b>Best Comments</b></p></th class="empty-row"><th></th><th></th><th class="table-danger"><p><b>Critical Comments</b></p></th></tr></thead>'
        for(let i = 0; i < bestComments.length; i++){
          tableCreation += '<tbody><tr><td scope="col" data-toggle="tooltip" title="'+bestComments[i]+'">' + smartTrim(bestComments[i], 50, " ", " ...") + '</td>';
          tableCreation += '<td scope="col"></td><td scope="col"></td>'
          if(worstComments!= null && worstComments.length !=0 && worstComments[i] !== undefined){
            tableCreation += '<td scope="col" data-toggle="tooltip" title="'+worstComments[i]+'">' + smartTrim(worstComments[i], 50, " "," ...") + '</td></tr>';
          } 
        }
        tableCreation += "</tbody></table>" 
      }
      
      document.getElementById(`mySim${video}`).innerHTML = tableCreation;

      if(similarity === undefined){
        $('div.myDiv').css('display','none');
        $('div.myDiv').css('display','none');
      }
      else{
        $('div.myDiv').css('display','inline');
      }
      
      entityCreation += "<nav id='toolbar' class='d-flex justify-content-left mb-4'>"
      if(entities != null){
        for(let i = 0; i < entities.length; i++){
          // entities[i]['entity']+ "\n" + entities[i]['type'] 
          entityCreation += "<button type='button' class='col-sm-2 btn btn-secondary mx-1'>"+ entities[i]['entity']+ "</button>";
        }
      }
      entityCreation += "</nav>" 
      document.getElementById(`collapseId${video}`).innerHTML = entityCreation;

      $('.modal').on('keydown', function (event) {
        if (event.keyCode === 27) {
          document.getElementById(`${title}close`).click();
        }
      });
      
      // Adding a null check for the wordCloudVal value
      if(wordCloudVal.length != 0){
      $(`#${vidId}`).jQWCloud({
        words: wordCloudVal,
        minFont: 13,
        maxFont: 50,
        padding_left: 1,
        // showSpaceDIV: true,
        // spaceDIVColor: 'white',
        word_common_classes: 'WordClass',
        word_mouseEnter: function () {
          $(this).css('text-decoration', 'underline');
        },
        word_mouseOut: function () {
          $(this).css('text-decoration', 'none');
        },
        word_mouseOver : function(){
          let link = $("<a>");
          let chosen_text = `${$(this).text()}`;
          link.attr("href", `https://en.wikipedia.org/w/index.php?title=${chosen_text}&printable=yes`);
          $(this).css('cursor','pointer').attr('title', link.attr("href"));
        },
        word_click: function () {
          // eslint-disable-next-line no-alert
          // This code will make the words in the word cloud clicable so as to navigate to the respective wiki pedia page.
          let link = $("<a>");
          let chosen_text = `${$(this).text()}`;
          link.attr("href", `https://en.wikipedia.org/w/index.php?title=${chosen_text}&printable=yes`);
          link.attr("title", "en.wikipedia.org");
          link.text(chosen_text);
          link.addClass("link");
          window.open(link.attr("href"), "_blank", "toolbar=yes,scrollbars=yes,resizable=yes,top=500,left=500,width=400,height=200");
        },
        beforeCloudRender: function () {
          date1 = new Date();
        },
      });
    }
  }
  }
  else{
    $('#loadContent').hideLoading();
    $('#errorPanel').css('display','inline');
    const errorHtml =`
    <div id="div" class="row">
    <img class="image col-sm-12" src="images/error_Smiley.PNG" width="100" height="300"/>
    </div>
    `;
    $('#errorPanel').find('#pills-error-panel').find('#errorContainer').find('.card').append(errorHtml);
  }
}

function eventGenerator(eventsAPI) {
  const locations = [];
  for (let event = 0; event < eventsAPI.length; event++) {
    let address = eventsAPI[event].address_line_1 + eventsAPI[event].address_line_2;

    // This is to make sure we don't display empty or zero values on the UI
    // Need to find possible workaround if possible : TO-DO
    if (address === 0) {
      address = '';
    }
    const eventCity = eventsAPI[event].city;
    const eventName = eventsAPI[event].name;
    const eventUrl = eventsAPI[event].url;
    // const eventDescp = eventsAPI[event].description;
    const startTime = eventsAPI[event].start_time_utc;
    const endTime = eventsAPI[event].end_time_utc;
    const eventSource = eventsAPI[event].source;
    const latitude = eventsAPI[event].lat;
    const longitude = eventsAPI[event].lng;


    const options = {
      weekday: 'long', year: 'numeric', month: 'long', day: 'numeric', hour: 'numeric', minute: 'numeric',
    };
    options.timeZone = 'UTC';
    let startDate = new Date(startTime);
    startDate = startDate.toLocaleDateString('en-US', options);
    let endDate = new Date(endTime);
    endDate = endDate.toLocaleDateString('en-US', options);
    if (eventSource === 'meetup') {
      image = 'images/EventBrite_logo.PNG';
    } else if (eventSource === 'eventbrite') {
      image = 'images/Meetup_logo.PNG';
    }
    const mapsHtml = `<div id="mapsEvent">
    <h7><b>${eventName} - ${eventCity}</b></h7>
    <h6><a href="${eventUrl}">${eventUrl}</a></h7>
    </div>`;

    locations.push([
      mapsHtml,
      latitude,
      longitude,
    ]);

    const eventHtml = ` 
      <div id="eventId" class="column">
        <div class="card border-info mb-2" style="max-width: 30rem;max-height: 30rem;"> 
            <div class="card-header text-white bg-info"><b>${eventName} - ${eventCity}</b></div>
                <iframe id="iframeID" src="https://maps.google.com/maps?q=${latitude},${longitude}&hl=en&z=14&amp;output=embed" 
                width="100%" height="400" frameborder="0" style="border:0" allowfullscreen></iframe>
                <div class="card-body"> 
                    <h5 class="card-title">${address}</h5>
                    <i class="fa fa-calendar fa-1x"></i><p class="card-text">${startDate} - ${endDate}</p>
                </div> 
                <div class="card-footer bg-transparent border-success text-center">
                      <a href="${eventUrl}"><i class="fa fa-globe fa-2x" aria-hidden="true"></i> WEBSITE </a>
                </div>
            </div>
      </div>
    `;
    $('#content').find('#pills-tabContent').find('#pills-events').find('.card-deck')
      .find('.row')
      .append(eventHtml);


    let marker; let j;
    const infowindow = new google.maps.InfoWindow();
    for (j = 0; j < locations.length; j++) {
      marker = new google.maps.Marker({
        position: new google.maps.LatLng(locations[j][1], locations[j][2]),
        map: map,
      });
      google.maps.event.addListener(
        marker, 'click',
        (function (marker, j) {
          return function () {
            infowindow.setContent(locations[j][0]);
            infowindow.open(map, marker);
          };
        })(marker, j),
      );
    }
  }
}

function visualiseData(videoUrl, chosenLanguage, source = 'cached') {
  if(source == 'cached'){
  videoPayload = {
    "params": {
      "query": chosenLanguage,
      "results_max_count": noOfCacheVideos,
      "source": source,
    },
  };
  }else{
    videoPayload = {
      "params": {
        "query": chosenLanguage,
        "results_max_count": noOfLiveVideos,
        "source": source,
      },
    };
  }

  // promise array for multiple API calls
  // One API for Video url and the other for event
  promiseArray = [getData(videoUrl, videoPayload)];
  Promise.all(promiseArray).then(allResponses => {
    console.log("API requets completed: " + videoUrl);
    videoResponse = allResponses[0];
    // check if the events flag is true then call events genarator
    resultsGenerator(chosenLanguage, videoResponse, true);
  });
}

function visualiseEventsData(eventsUrl, chosenLanguage) {
  eventsPayload = {
    'keyword': chosenLanguage ,
    'lat': 53.3498,
    'lng': -6.2603,
  };
  // promise array for multiple API calls
  promiseArray = [getData(eventsUrl, eventsPayload)]
  Promise.all(promiseArray).then(allResponses => {
    console.log("API requets completed: " + eventsUrl);
    eventsResponse = allResponses[0];
    // replace apiMockupData with data from response when API is ready
    eventGenerator(eventsResponse);
  });

  // eslint-disable-next-line no-unused-vars
  const map = new google.maps.Map(document.getElementById('map'), {
    zoom: 10,
    center: new google.maps.LatLng(eventsPayload.lat, eventsPayload.lng),
    mapTypeId: google.maps.MapTypeId.ROADMAP,
  });
}

function populateTextBox(value){
  if(value != ' '){
    $('div#mainMenu').find('.imgtext').find('#justLogo').find('#searchForm').find('#textBoxId').val(value);
  }
}

function callCommonMethods(){
  collapseOnClick();
  reset();
  loading();
  addButtons();
}

function feedbackOptionDisplay(){
  $(".open").on("click", function() {
    $(".popup-overlay, .popup-content").addClass("active");
  });
  
  //removes the "active" class to .popup and .popup-content when the "Close" button is clicked 
  $(".close, .popup-overlay").on("click", function() {
    $(".popup-overlay, .popup-content").removeClass("active");
  });
}
function collapseOnClick(){
  $('div#mainMenu').find('.row').find('#aboutId').animate({ fontsize: '10px',});
    $('div#mainMenu').find('h5#slogan').css('display','none');
    $('div#mainMenu').find('#logoId').css('display','none');
    $('div#mainMenu').find('#justLogo').css('display','inline');
    $('div#mainMenu').find('.row').find('#justLogo').animate({ height: '60px', paddingLeft : '10px',}); 
    $('div#mainMenu').find('.container').find('nav#toolbar').animate({ height: '0px',});
    $('div#mainMenu').find('.container').find('nav#toolbar').css('display','none');
    $('div#mainMenu').find('#oldmain').css('display','none')
    $('div#mainMenu').find('.container').find('#searchForm').animate({ 
      height: '40px', 
      marginBotton : "0in", 
    });
    $('div#mainMenu').find('.container').css('display','none')
    $('div#mainMenu').find('#sectionId').find('.navbarVal')
      .find('#pills-tab').css('display','none');
    $('div#mainMenu').find('#sectionId').find('.navbarVal')
      .find('#pills-tab').animate({ 
        height: '800px',    
        marginTop : '0in',
    });
}

function reset() {
  $('button#sortDesc').addClass('disabled'); 
  $('button#sortAsc').addClass('disabled');
  // remove the more info id from the previous request
  $('div').remove('#moreInfoDiv');
  // This code will reset the video tab everytime the button is clicked
  $('div').remove('#mainId');
  // This code will reset the events tab everytime the button is clicked
  $('div').remove('#eventId');
}

function hideNavbar(){
  $('div#content').hide();
}

function loading(){
  $('#loadContent').showLoading();
}

function enableButtons() {
  $('button#sortDesc').addClass('enabled'); 
  $('button#sortAsc').addClass('enabled'); 
  $('div#content').show();
}

function removeButtons() {
  $('div#content').find('#sectionId').find('.navbarVal')
      .find('#pills-tab').css('display','none');
  $('div#content').find('#sectionId').find('#pills-tabContent').find('#pills-video')
      .find('#container').find('#dropdownMenuButton').css('display','none');
}

function addButtons(){
  $('button#sortDesc').css('display','inline');
  $('button#sortAsc').css('display','inline');
}
function getPositionData(position) {
  lat = position.coords.latitude;
  lng = position.coords.longitude;

  map = new google.maps.Map(document.getElementById('map'), {
    zoom: 10,
    center: new google.maps.LatLng(lat, lng),
    mapTypeId: google.maps.MapTypeId.ROADMAP,
  });
}

function loadMapWithPosition() {
    if (navigator.geolocation) {
      navigator.geolocation.getCurrentPosition(getPositionData);
    } else {
      console.log('Geolocation is not supported by this browser.');
    }
}

// eslint-disable-next-line no-unused-vars
function initMap() {
  loadMapWithPosition();
  
}

$(document).ready(() => {
  feedbackOptionDisplay();
  $('div#content').hide();
  $('div#mainMenu').find('.container').find('#searchForm').find('#textBoxId').keypress(function(event){
      var keycode = (event.keyCode ? event.keyCode : event.which);
      if(keycode == '13'){
        let textBoxVal = $('div#mainMenu').find('.container').find('#searchForm').find('#textBoxId').val();
        if(textBoxVal != ''){
          $('div#mainMenu').find('.imgtext').find('#justLogo').find('#searchForm').find('#textBoxId').val(textBoxVal)  
          collapseOnClick();
          event.preventDefault();
          hideNavbar();
          reset();
          loading();
          visualiseData(videoUrl, textBoxVal, "live");
          visualiseEventsData(eventsUrl, textBoxVal);	
        }
	    }
  });

  $('div#mainMenu').find('.imgtext').find('#justLogo').find('#searchForm').find('#textBoxId').keypress(function(event){
    var keycode = (event.keyCode ? event.keyCode : event.which);
    if(keycode == '13'){
      let textBoxVal = $('div#mainMenu').find('.imgtext').find('#justLogo').find('#searchForm').find('#textBoxId').val();
      if(textBoxVal != ''){
        event.preventDefault();
        hideNavbar();
        reset();
        loading();
        visualiseData(videoUrl, textBoxVal, "live");
        visualiseEventsData(eventsUrl, textBoxVal);	
      }
    }
  });

  // what action needs to be performed whwn the serach button is clicked
  $('div#mainMenu').find('.container').find('#searchForm').find('#searchButtonId').click(function () {
    // reset other data in the events and maps tab
    let textBoxVal = $('div#mainMenu').find('.container').find('#searchForm').find('#textBoxId').val();
    if(textBoxVal != ''){
      $('div#mainMenu').find('.imgtext').find('#justLogo').find('#searchForm').find('#textBoxId').val(textBoxVal)  
      collapseOnClick();
      hideNavbar();
      reset();
      loading();
      visualiseData(videoUrl, textBoxVal, "live");
      visualiseEventsData(eventsUrl, textBoxVal);
    }
  });

  $('div#mainMenu').find('.imgtext').find('#justLogo').find('#searchForm').find('#searchButtonId').click(function () {
    // reset other data in the events and maps tab
    let textBoxVal = $('div#mainMenu').find('.imgtext').find('#justLogo').find('#searchForm').find('#textBoxId').val();
    if(textBoxVal != ''){
      hideNavbar();
      reset();
      loading();
      visualiseData(videoUrl, textBoxVal, "live");
      visualiseEventsData(eventsUrl, textBoxVal);
    }
  });

  $('#python').click(function () {
    populateTextBox('Python');
    callCommonMethods();
    visualiseData(videoUrl, 'Python');
    visualiseEventsData(eventsUrl, 'Python');
  });

  $('#java').click(function () {
    populateTextBox('Java');
    callCommonMethods();
    visualiseData(videoUrl, 'Java');
    visualiseEventsData(eventsUrl, 'Java');
  });

  $('#cassandra').click(function () {
    populateTextBox('Cassandra');
    callCommonMethods();
    visualiseData(videoUrl, 'Cassandra');
    visualiseEventsData(eventsUrl, 'Cassandra');
  });

  $('#hadoop').click(function () {
    populateTextBox('Hadoop');
    callCommonMethods();
    visualiseData(videoUrl, 'Hadoop');
    visualiseEventsData(eventsUrl, 'Hadoop');
  });

  $('#fsharp').click(function () {
    populateTextBox('F#');
    callCommonMethods();
    visualiseData(videoUrl, 'F#');
    visualiseEventsData(eventsUrl, 'F#');
  });

  $('#rProgramming').click(function () {
    populateTextBox('R Programming');
    callCommonMethods();
    visualiseData(videoUrl, 'R programming');
    visualiseEventsData(eventsUrl, 'R programming');
  });

  $('div#content').find('#sectionId').find('#pills-tabContent')
  .find('#pills-video').find('#container').find('.dropdown-menu').find('#sortDesc')
    .click(function () {
      // reset other data in the events and maps tab
      reset();
      loading();
      resultsGenerator('',videoResponse, 'desc');
      eventGenerator(eventsResponse);
    });

    $('div#content').find('#sectionId').find('#pills-tabContent')
    .find('#pills-video').find('#container').find('.dropdown-menu').find('#sortAsc')
    .click(function () {
      // reset other data in the events and maps tab
      reset();
      loading();
      resultsGenerator('',videoResponse, 'asc');
      eventGenerator(eventsResponse);
    });
    $('div#content').find('#sectionId').find('#pills-tabContent')
    .find('#pills-video').find('#container').find('.dropdown-menu').find('#rankOrder')
    .click(function () {
      // reset other data in the events and maps tab
      reset();
      loading();
      resultsGenerator('',videoResponse, 'rankOrder');
      eventGenerator(eventsResponse);
    });
});