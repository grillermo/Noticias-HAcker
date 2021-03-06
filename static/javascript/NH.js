function markAsRead(self, notification_key){
  $.get('/inbox/marcar-como-leido/' + notification_key, function(data) {
    if (data == 'Ok'){
      $(self).parents(".notification").hide();
    } else if (data == 'Bad'){
      window.location = "/login"
    }
  });
}

function upVote(self, post_key){
  $.get('/upvote/' + post_key, function(data) {
    if (data == 'Ok'){
      self.className += " voted";
      var current_counter = $(self).closest('.noticia').find('.sum_votes');
      var current_count = parseInt(current_counter.html());
      var new_count = current_count + 1;
      current_counter.html(new_count);
    } else if (data == 'Bad'){
      window.location = "/login"
    }
  });
}
function upVoteComment(self, post_key){
  $.get('/upvote_comment/' + post_key, function(data) {
    if (data == 'Ok'){
      self.className += " voted";
    } else if (data == 'Bad'){
      window.location = "/login"
    }
  });
}

/**
 * Simple validacion de http://www.anieto2k.com/2008/06/25/validar-formularios-con-jquery/
 */
var filters = {
    requerido: function(el) {return ($(el).val() != '' && $(el).val() != -1);},
    email: function(el) {
        if ($(el).val() != '') {
            /**
             * Regexp from: http://fightingforalostcause.net/misc/2006/compare-email-regex.php
             */
            return /^([\w\!\#$\%\&\'\*\+\-\/\=\?\^\`{\|\}\~]+\.)*[\w\!\#$\%\&\'\*\+\-\/\=\?\^\`{\|\}\~]+@((((([a-z0-9]{1}[a-z0-9\-]{0,62}[a-z0-9]{1})|[a-z])\.)+[a-z]{2,6})|(\d{1,3}\.){3}\d{1,3}(\:\d{1,5})?)$/i.test($(el).val());
        }
        return true;
    },
    url: function(el) {
        if ($(el).val() != '') {
            return /(ftp|http|https):\/\/(\w+:{0,1}\w*@)?(\S+)(:[0-9]+)?(\/|\/([\w#!:.?+=&%@!\-\/]))?/.test($(el).val());
        }
        return true;
    }
};

// Extensiones
$.extend({
  stop: function(e){
    if (e.preventDefault) e.preventDefault();
    if (e.stopPropagation) e.stopPropagation();
  }
});

$(document).ready(function() {
  $("form.validable").bind("submit", function(e){
  	if (typeof filters == 'undefined') return;
    $(this).find("input, textarea, select").each(function(x,el){
      if ($(el).attr("className") != 'undefined') {
        $.each(new String($(el).attr("className")).split(" "), function(x, klass){
          if ($.isFunction(filters[klass]))
            if (!filters[klass](el))  $(el).addClass("fielderror");
        });
      }
    });
    if ($(this).find(".fielderror").size() > 0) {
      $.stop(e || window.event);
      return false;
    }
    return true;
  });

  $('.fielderror').live('blur', function() {
    if ($(this).val() != '') {
      $(this).removeClass('fielderror');
    }
  });

  $('.hide-show-comment').show();
  $('#post').delegate('.hide-show-comment','click',function(){
	comment = $(this).closest('.comment');
	if($(this).html() == '[-]'){
		$(this).html('[+]');
		$('> .comment-message, > .innerComments, > .reply, > .votes',comment).hide();
	}else{
		$(this).html('[-]');
		$('> .comment-message, > .innerComments, > .reply, > .votes',comment).show();
	}

  });
});
