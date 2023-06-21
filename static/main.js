/**
 * Returns the current datetime for the message creation.
 */
function getCurrentTimestamp() {
	return new Date();
}

/**
 * Renders a message on the chat screen based on the given arguments.
 * This is called from the `showUserMessage` and `showBotMessage`.
 */
function renderMessageToScreen(args) {
	// local variables
	let displayDate = (args.time || getCurrentTimestamp()).toLocaleString('en-IN', {
		month: 'short',
		day: 'numeric',
		hour: 'numeric',
		minute: 'numeric',
	});
	let messagesContainer = $('.messages');

	// init element
	let message = $(`
	<li class="message ${args.message_side}">
		<div class="avatar"></div>
		<div class="text_wrapper">
			<div class="text">${args.text}</div>
			<div class="timestamp">${displayDate}</div>
		</div>
	</li>
	`);

	// add to parent
	messagesContainer.append(message);

	// animations
	setTimeout(function () {
		message.addClass('appeared');
	}, 0);
	messagesContainer.animate({ scrollTop: messagesContainer.prop('scrollHeight') }, 300);
}

/**
 * Displays the user message on the chat screen. This is the right side message.
 */
function showUserMessage(message, datetime) {
	renderMessageToScreen({
		text: message,
		time: datetime,
		message_side: 'right',
	});
}

/**
 * Displays the chatbot message on the chat screen. This is the left side message.
 */
function showBotMessage(message, datetime) {
	renderMessageToScreen({
		text: message,
		time: datetime,
		message_side: 'left',
	});
}

/**
 * Get input from user and show it on screen on button click.
 */
/**
 * Function to send user message when Enter key is pressed.
 */
$('#msg_input').keypress(function (e) {
    if (e.which == 13) { // Enter key = keycode 13
        $('#send_button').click(); // Trigger send button click event
        return false; // Prevent form submission
    }
});


/**
 * Get input from user and show it on screen on button click.
 */
$('#send_button').on('click', function (e) {
    var userMsg = $('#msg_input').val();

    // get and show message and reset input
    showUserMessage(userMsg);
    $('#msg_input').val('');

    // show loading spinner
    $('#loading_spinner').show();

    // get response from server
    $.ajax({
        url: '/get',
        method: 'POST',
        data: { msg: userMsg },
        success: function(data) {
            // hide loading spinner
            $('#loading_spinner').hide();

            // parse JSON response and extract message(s) by key
            for (var key in data) {
                if (data.hasOwnProperty(key)) {
                    let sectionTitle = '<strong>' + key + '</strong>';
                    let sectionResponse = data[key];

                    setTimeout(function () {
                        showBotMessage(sectionTitle + ': ' + sectionResponse);
                    }, 300);
                }
            }
        },
        error: function() {
            // hide loading spinner
            $('#loading_spinner').hide();

            setTimeout(function () {
                showBotMessage('Sorry, I am currently unable to provide a response.');
            }, 500);
        }
    });
});



var questions = [
	"What are the strategic dependencies of the 'SAP_re_implementation-programme_2' project?",
    "Which mitigation strategies are linked to the 'Poor_project_execution' risk?",
    "What is the supply chain strategy associated with the 'Digital_Supply_Chain:' strategy theme?",
    "Which programme is associated with the 'Winning_with_brands_and_innovation' service offering?",
    "What are the risks associated with the 'Business_disruption_' project risk?",
    "Which areas of support are provided for the 'Org._transformation_programme_1'?",
    "What are the value creation models for the 'Value_theme' strategy?",
    "How is the 'Acquisition_programme_1' linked with the 'Partnerships_for_the_future:' strategy theme?",
    "What are the strategic dependencies for the 'Net_Revenue_Mgt_programme'?",
    "What is the supply chain strategy for the '3._Logistics' value Unilever creates?",
    "How does the 'Innovation_theme' connect with our service offerings?",
    "What risks are associated with the 'Brexit_Programme' and what are their mitigations?",
    "How is 'Executive_sponsorship' involved in 'Business_Transformation_themes'?",
    "How does the 'Talent_&_Capabilities:' strategy theme relate to the 'UK_Operations'?",
    "What Q4 triggers are associated with the 'Systems_integration_programme'?",
    "How does the '5S_Smart_Programme' contribute to the 'Value_Unilever_create'?",
    "Which programmes are connected to the 'Responsible_and_Sustainable_Living__theme' strategy theme?",
    "What is the role of 'Steering_group' in the context of 'Project' node?",
    "How is the 'Agility_for_a_Changing_Market:_' strategy theme related to 'Our_Service_Offerings'?",
    "Which 'Areas_of_support' are involved in the 'Data_management_enhancement_programme_2'?",
	"What are project risks associated with your supply chain strategies?",
    "What types of business value does Unilever create?",
    "How many types of strategy themes are there? Could you please provide their names?",
    "How many types of support areas are there? Could you please provide their names?",
    "How many types of mitigation are there? Could you please provide their names?"
];

var list = document.getElementById('question-list');

for (var i = 0; i < questions.length; i++) {
    var listItem = document.createElement('li');
    listItem.textContent = questions[i];
    list.appendChild(listItem);
}

/**
 * Returns a random string. Just to specify bot message to the user.
 */
function randomstring(length = 20) {
	let output = '';

	// magic function
	var randomchar = function () {
		var n = Math.floor(Math.random() * 62);
		if (n < 10) return n;
		if (n < 36) return String.fromCharCode(n + 55);
		return String.fromCharCode(n + 61);
	};

	while (output.length < length) output += randomchar();
	return output;
}

/**
 * Set initial bot message to the screen for the user.
 */
$(window).on('load', function () {
	showBotMessage('Hi, there! I am a Chatbot specialised in communicating with Graph Databases.');
});
