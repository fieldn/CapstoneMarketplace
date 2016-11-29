/*
	Project: CSCapstone Marketplace
*/


$(document).ready(function() { 
	$(".sortable").tablesorter();
	$('.validate').bValidator();

	$(".datepicker").datepicker({
		dateFormat: 'yy-mm-dd',
	});


	function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = $.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
	}
	var csrftoken = getCookie('csrftoken');

	function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});

function timeDifference(current, previous) {
    var msPerMinute = 60 * 1000
    var msPerHour = msPerMinute * 60
    var msPerDay = msPerHour * 24
    var msPerMonth = msPerDay * 30
    var msPerYear = msPerDay * 365

    var elapsed = current - previous

    if (elapsed < msPerMinute)
         return Math.round(elapsed/1000) + ' seconds ago'
    else if (elapsed < msPerHour)
         return Math.round(elapsed/msPerMinute) + ' minutes ago'
    else if (elapsed < msPerDay )
         return Math.round(elapsed/msPerHour ) + ' hours ago'
    else if (elapsed < msPerMonth)
        return 'approximately ' + Math.round(elapsed/msPerDay) + ' days ago'
    else if (elapsed < msPerYear)
        return 'approximately ' + Math.round(elapsed/msPerMonth) + ' months ago'
    else
        return 'approximately ' + Math.round(elapsed/msPerYear ) + ' years ago'   
}

	$("#comments").html(function g (html, commentsList) {
		return html + '<ul>' + commentsList.map(e => {
			const sub = e.subcomments.length ? g(html, e.subcomments) : '' 
			const timeStr = timeDifference(Date.now(), new Date(e.time))
			return `<li><p style="color: gray">${timeStr}</p><p data-id=${e.id}>${e.comment}<p>${sub} </li>`
		}).join('') + '</ul>'
	}('', $("#data").data('comments').list) + '<p data-id=-1>Click to add a comment</p>')

	let li = null;

	$("#comments").click(e => {
		const $target = $(e.target)
		const parentId = e.target.dataset.id

		if (!parentId) return

		if (li)
			li.remove()
		li = $('<li>')
		let button = $('<input type=button value=Submit>')
		let inputBox = $('<input>')
		li.append(inputBox)
		li.append(button) 
		button.click(e => {
			$.post('/addcomment', {
				comment: inputBox.val(),
				id: parentId
			}, data => {
				location.reload()
			})
		})
		if (!$target.children().length)
			$target.append(li)
		else
			$target.children().first().prepend(li)
	});
})
