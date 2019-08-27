/** A javascript file which is used to fetch the feedback rekated data on click from the user and this will be stored in the database usng the API endpoint
 * /api/V1.0/feedback 
 */

function WriteFeedbackToDB(feedBackUrl, feedbackVal) {
	feedbackPayload = {
		"params": {
		  "feedback": feedbackVal
		}
	  };
  
	// promise array for multiple API calls
	// One API for Video url and the other for event
	promiseArray = [getData(feedBackUrl, feedbackPayload)];
	Promise.all(promiseArray).then(allResponses => {
	  feedbackResponse = allResponses[0];
	  if(feedbackResponse["message"] == "feedback record success"){
		  console.log('Feedback written succesfully')
	  } 
	});
  }

  $(document).ready(() => {
	$('div#mainMenu').find("#myModal").find('#veryhappy').click(function(){
		WriteFeedbackToDB(feedBackUrl, 4)
		alert("Thanks for taking time and voting")
	  });

	$('div#mainMenu').find("#myModal").find('#happy').click(function(){
		WriteFeedbackToDB(feedBackUrl, 3)
		alert("Thanks for taking time and voting")
	});

	$('div#mainMenu').find("#myModal").find('#average').click(function(){
		WriteFeedbackToDB(feedBackUrl, 2)
		alert("Thanks for taking time and voting")
	});

	$('div#mainMenu').find("#myModal").find('#sad').click(function(){
		WriteFeedbackToDB(feedBackUrl, 1)
		alert("Thanks for taking time and voting")
	});
  });