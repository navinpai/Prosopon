(function() {
    var kSignInText = 'Sign in with your e-mail',
        kSignOutText = 'Sign out';

    var action_button = document.querySelector('.persona-button');
    var button_text = document.querySelector('.persona-button span');
    var whoami_text = document.querySelector('.whoami');

    function onButtonClick(ev) {
        if (kSignInText == button_text.innerHTML) {
            navigator.id.request();
        } else {
            navigator.id.logout();
        }
    }

    function signedIn(identifier) {
        button_text.textContent = kSignOutText;
        whoami_text.textContent = identifier;
    }

    function signedOut() {
        button_text.textContent = kSignInText;
        whoami_text.textContent = 'Anonymous';
    }

    function updateIdentifier(assertion, callback) {
        var path = null === assertion ? '/signout' : '/signin';
        var request = new XMLHttpRequest();
        request.open('POST', path, false);
        request.setRequestHeader('content-type', 'application/json');
        request.onreadystatechange = function(rev) {
            if (4 == request.readyState) {
                if (200 == request.status) {
                    var result = JSON.parse(request.responseText);
                    if ('success' == result.status) {
                        callback(result.identifier);
                    } else {
                        console.log("Error: ", result);
                        navigator.id.logout();
                    }
                } else {
                    console.log("Error: ", request.responseText);
                    navigator.id.logout();
                }
            }
        };
        request.send(JSON.stringify({assertion: assertion}));
    }
    var loggedInUser = whoami_text.textContent == 'Anonymous' ?
        null : whoami_text.textContent;
    navigator.id.watch({
        loggedInUser: loggedInUser,
        onlogin: function(assertion) {
            updateIdentifier(assertion, signedIn);
        },
        onlogout: function() {
            updateIdentifier(null, signedOut);
        }
    });
    action_button.addEventListener('click', onButtonClick, false);
})();
