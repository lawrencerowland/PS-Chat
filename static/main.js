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

    // Convert the source into a string of HTML paragraphs
    // Each source will be wrapped into its own collapsible section
    let sourceBox = '';
    if (args.source) {
        if (Array.isArray(args.source)) {
            args.source.forEach((src, idx) => {
                sourceBox += `
                <button class="collapsible" id="collapsible-${idx}">Show Source ${idx + 1}</button>
                <div class="content">
                    <p>${src}</p>
                </div>
                `;
            });
        } else {
            sourceBox = `
            <button class="collapsible">Show Source</button>
            <div class="content">
                <p>${args.source}</p>
            </div>
            `;
        }
    }

    // init element
    let message = $(`
    <li class="message ${args.message_side}">
        <div class="avatar"></div>
        <div class="text_wrapper">
            <div class="text">${args.text}</div>
            ${sourceBox}
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

    // Event listener for the collapsible box
    $('.collapsible').on('click', function() {
        this.classList.toggle('active');
        var content = this.nextElementSibling;
        if (content.style.display === "block") {
            content.style.display = "none";
        } else {
            content.style.display = "block";
        }
    });
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
 function showBotMessage(message, datetime, source) {
    renderMessageToScreen({
        text: message,
        time: datetime,
        message_side: 'left',
        source: source
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

    // Collect all checked namespaces.
    var namespaces = [];
    $(".form-check-input:checked").each(function() {
        namespaces.push($(this).val());
    });
    var selectedChatMode = $(".chat-mode:checked").val();
    // print (selectedChatMode)
    // get and show message and reset input
    showUserMessage(userMsg);
    $('#msg_input').val('');

    // show loading spinner
    $('#loading_spinner').show();

    // get response from server
    // get response from server
    $.ajax({
        url: '/get',
        method: 'POST',
        data: { msg: userMsg,
            namespace: JSON.stringify(namespaces),
            chat_mode: JSON.stringify(selectedChatMode)
        },
        success: function(data) {
            // hide loading spinner
            $('#loading_spinner').hide();

            // parse JSON response and extract message(s) by key
            for (var key in data) {
                if (data.hasOwnProperty(key)) {
                    let sectionTitle = '<strong>' + key + '</strong>';
                    let sectionResponse = data[key]["text"];
                    let sectionSource = data[key]['source'];  // Assuming 'source' is the key for the additional information

                    setTimeout(function () {
                        showBotMessage(sectionTitle + ': ' + sectionResponse, undefined, sectionSource);
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
	showBotMessage('Hi, there! I am a Chatbot specialised in project management');
});