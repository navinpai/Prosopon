(function() {
    var visitors_list = document.getElementById('visitors_list');

    function populateList(visitors, me) {
        visitors_list.innerHTML = '';
        var foundMe = false;
        for(var i = 0, v; v = visitors[i]; i++) {
            var li = document.createElement('li');
            li.textContent = (v.identifier +
                    (v.id == me ? ' (This is you)' : '') +
                    ' last visited ' + v.lastpath +
                    ' at ' + v.lastvisit);
            visitors_list.appendChild(li);
            foundMe = foundMe || v.id == me;
        }
        // Ensure that we're logged out if we've been pruned by the server.
        if (!foundMe) {
            navigator.id.logout();
        }
    }

    function refreshVisitors() {
        var request = new XMLHttpRequest();
        request.open('GET', '/visitors', false);
        request.onreadystatechange = function(rev) {
            if (4 == request.readyState) {
                if (200 == request.status) {
                    var payload = JSON.parse(request.responseText);
                    populateList(payload.visitors, payload.me);
                    scheduleRefresh();
                } else {
                    console.log("Error: ", request.responseText);
                }
            }
        };
        request.send(null);
    }

    function scheduleRefresh() {
        window.setTimeout(refreshVisitors, 3000);
    }
    scheduleRefresh();
})();
