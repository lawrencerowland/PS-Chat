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
                    }, 500);
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



var low_level_questions = [
    "What are the strategic dependencies of our ongoing technological implementation projects?",
    "Which mitigation strategies are linked to the risk of poor project execution?",
    "What is our supply chain strategy associated with digital transformation?",
    "Which programmes are associated with winning through brand innovation and market competitiveness?",
    "What are the risks associated with potential business disruptions?",
    "Which areas of support are provided for our ongoing organizational transformation programmes?",
    "What models are we using for creating strategic value?",
    "How are our acquisition programmes linked with future partnerships strategies?",
    "What are the strategic dependencies for our net revenue management programme?",
    "What is our supply chain strategy for our logistics operations?",
    "How does innovation connect with our service offerings?",
    "What risks are associated with our strategic response to major geopolitical changes and what are their mitigations?",
    "How is executive sponsorship involved in our business transformation themes?",
    "How do our talent and capabilities strategies relate to our operations in specific regions?",
    "What key events or triggers are associated with our systems integration programmes?",
    "How do our strategic initiatives contribute to value creation?",
    "Which programmes are connected to the theme of responsible and sustainable living?",
    "What is the role of steering groups in the context of project management?",
    "How is our strategy theme related to agility and change management related to our service offerings?",
    "Which areas of support are involved in our data management enhancement programmes?"
];

var list = document.getElementById('question-list');
for (var i = 0; i < low_level_questions.length; i++) {
    var listItem = document.createElement('li');
    listItem.textContent = low_level_questions[i];
    list.appendChild(listItem);
}

var high_level_questions = [
    "What impact could poor project execution have on our ongoing acquisitions and disposals?",
    "How are we ensuring non-delivery of benefits risk is being mitigated in our revenue management programmes?",
    "What steps are we taking to prevent business disruption as a result of our strategic initiatives?",
    "How are we managing the risk of slowing digitisation pace in our supply chain themes?",
    "In what ways could a slowed technological change risk affect our data management enhancement programmes?",
    "How can we ensure that executive sponsorship and steering groups are effectively supporting our organizational transformation initiatives?",
    "Are regular progress updates being maintained for our key strategic initiatives and are there any significant updates?",
    "How are our links with digital programme teams contributing to systems integration efforts?",
    "Are appropriate personnel assigned for critical technological implementations?",
    "How are we monitoring the volume of our change programmes?",
    "Are we aligning our innovation and sourcing efforts with our overall value creation strategies?",
    "How is our talent and capabilities theme being reflected in our project acquisitions?",
    "Are our leadership standards being followed in all our project management practices?",
    "How is our supply chain strategy being applied to our key operational areas?",
    "In the context of business transformation themes, how are we handling the risks and challenges associated with our operations?"
]
var list = document.getElementById('question-list2');
for (var i = 0; i < high_level_questions.length; i++) {
    var listItem = document.createElement('li');
    listItem.textContent = high_level_questions[i];
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
